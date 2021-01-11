import graphene
import graphql_social_auth
from django.db import IntegrityError
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import User, Contact, Template
from graphql import GraphQLError

from .views import welcome_mail


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'username', 'email', 'gender', 'phone', 'bio',
                  'languages', 'location', 'date_of_birth', 'profession', 'profile_pix',)


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = '__all__'


class TemplateType(DjangoObjectType):
    class Meta:
        model = Template
        fields = ('id', 'name',)


class Query(graphene.ObjectType):
    personal_info = graphene.Field(UserType, username=graphene.String())
    template = graphene.Field(graphene.List(TemplateType))

    def resolve_personal_info(self, info, username):
        try:
            return User.objects.get(username=username)
        except Exception:
            raise GraphQLError("User not found")

    def resolve_template(self, info):
        return Template.objects.all()


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


class TemplateMutation(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        try:
            User.objects.get(username=info.context.user.username).update(template=id)
            return TemplateMutation(ok=True)
        except User.DoesNotExist:
            return TemplateMutation(ok=False, warning="User not found!")


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
                                     email=kwargs['email'], password=kwargs['password'], username=kwargs['last_name'])
        except IntegrityError:
            return Registration(ok=False, error="Email already exist")
        return Registration(ok=True)


class ContactMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        email = graphene.String(required=True)
        message = graphene.String(required=True)
        fullName = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        Contact.objects.create(full_name=kwargs['fullName'], message=kwargs['message'], email=kwargs['email'])
        return ContactMutation(ok=True)


class Mutation(graphene.ObjectType):
    social_auth = graphql_social_auth.SocialAuthJWT.Field()
    personal_info = PersonalInformationMutation.Field()
    contact = ContactMutation.Field()
    register = Registration.Field()
    template = TemplateMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
