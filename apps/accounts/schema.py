import cloudinary
import graphene
import graphql_social_auth

from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required

from .models import User, Contact
from .forms import PersonalInformationForm, ContactForm
from graphql import GraphQLError


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'username', 'email', 'gender', 'phone', 'bio', 'resume',
                  'languages', 'nationality', 'state_of_residence', 'date_of_birth', 'profession', 'profile_pix', 'id')


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = '__all__'


class Query(graphene.ObjectType):
    get_personal_info = graphene.Field(UserType, username=graphene.String())

    def resolve_get_personal_info(self, info, username):
        try:
            return User.objects.get(username=username)
        except Exception:
            raise GraphQLError("User not found")


class PersonalInformationMutation(DjangoModelFormMutation):
    user = graphene.Field(UserType)
    ok = graphene.Boolean()

    class Meta:
        form_class = PersonalInformationForm

    @login_required
    def perform_mutate(self, info):
        user, created = User.objects.update_or_create(
            username=info.context.user.username,
            defaults=self.data
        )
        return PersonalInformationMutation(ok=True, user=user)


class Avatar(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        avatar = graphene.String(required=True)

    @login_required
    def mutate(self, info, avatar):
        try:
            user = info.context.user
            image = cloudinary.uploader.upload(avatar)
            user.profile_pix = image['url']
            user.save()
            return Avatar(ok=True)
        except Exception as ex:
            print("An error occured \n", ex)
            return Avatar(ok=False)


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
    avatar = Avatar.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
