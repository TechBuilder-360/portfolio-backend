import graphene
from django.forms import forms
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation, DjangoFormMutation
from .models import User
from .forms import RegistrationForm, PersonalInformationForm, PasswordChangeForm


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'gender', 'phone', 'bio', 'resume', 'languages',
                  'nationality', 'state_of_residence', 'status', 'date_of_birth', 'profession', 'profile_pix', 'id')


class Query(graphene.ObjectType):
    get_personal_info = graphene.Field(UserType, id=graphene.Int())

    def resolve_get_personal_info(self, info, id):
        user = User.objects.get(id=id)
        if user:
            return user
        else:
            return User.DoesNotExist


class UserRegistrationMutation(DjangoModelFormMutation):
    user = graphene.Field(UserType)

    class Meta:
        form_class = RegistrationForm


class LoginMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = User.objects.get(email=email)
        if not user:
            raise forms.ValidationError("User does not exist")
        if user.check_password(password):
            return LoginMutation(user)
        raise forms.ValidationError("Incorrect credentials")


class PasswordChangeMutation(DjangoFormMutation):
    user = graphene.Field(UserType)

    class Meta:
        form_class = PasswordChangeForm


class PersonalInformationMutation(DjangoModelFormMutation):
    user = graphene.Field(UserType)

    class Meta:
        form_class = PersonalInformationForm


class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
    create_user = UserRegistrationMutation.Field()
    change_password = PasswordChangeMutation.Field()
    personal_info = PersonalInformationMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)