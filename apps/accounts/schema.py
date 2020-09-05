import graphene
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


class PasswordChangeMutation(DjangoFormMutation):
    user = graphene.Field(UserType)

    class Meta:
        form_class = PasswordChangeForm


class PersonalInformationMutation(DjangoModelFormMutation):
    user = graphene.Field(UserType)

    class Meta:
        form_class = PersonalInformationForm


class Mutation(graphene.ObjectType):
    create_user = UserRegistrationMutation.Field()
    change_password = PasswordChangeMutation.Field()
    personal_info = PersonalInformationMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)