import cloudinary
import graphene
import graphql_social_auth
from django.db import IntegrityError
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required
from .models import User, Contact
from .forms import ContactForm
from graphql import GraphQLError
from .views import send_mail


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'username', 'email', 'gender', 'phone', 'bio',
                  'languages', 'location', 'date_of_birth', 'profession', 'profile_pix')


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = '__all__'


class Query(graphene.ObjectType):
    personal_info = graphene.Field(UserType, username=graphene.String())

    def resolve_personal_info(self, info, username):
        try:
            return User.objects.get(username=username)
        except Exception:
            raise GraphQLError("User not found")


class PersonalInformationMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        middle_name = graphene.String()
        email = graphene.String(required=True)
        gender = graphene.String()
        phone = graphene.String()
        bio = graphene.String()
        languages = graphene.String()
        location = graphene.String()
        date_of_birth = graphene.Date()
        profession = graphene.String()

    @login_required
    def mutate(self, info, **data):
        User.objects.update_or_create(
            username=info.context.user.username,
            email=info.context.user.email,
            defaults=data
        )
        return PersonalInformationMutation(ok=True)


class Registration(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        try:
            User.objects.create_user(last_name=kwargs['last_name'], first_name=kwargs['first_name'],
                                     email=kwargs['email'], password=kwargs['password'])
        except IntegrityError:
            return Registration(ok=False, error="Email already exist")
        send_mail(user=info.context.user)  # Todo send welcome email
        return Registration(ok=True)


class UploadMutation(graphene.Mutation):
    class Arguments:
        file = graphene.String(required=True)

    success = graphene.Boolean()

    # @login_required
    def mutate(self, info, file, **kwargs):
        try:
            user = info.context.user
            image = cloudinary.uploader.upload(file)
            info.profile_pix = image['url']
            user.save()
            return UploadMutation(success=True)
        except Exception as ex:
            return UploadMutation(success=False)


class ContactMutation(DjangoModelFormMutation):
    ok = graphene.Boolean()

    class Meta:
        form_class = ContactForm

    def perform_mutate(self, info):
        self.save()
        ok = True
        return ContactMutation(ok=ok)


class Mutation(graphene.ObjectType):
    social_auth = graphql_social_auth.SocialAuthJWT.Field()
    personal_info = PersonalInformationMutation.Field()
    contact = ContactMutation.Field()
    upload = UploadMutation.Field()
    register = Registration.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
