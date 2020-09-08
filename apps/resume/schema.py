import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from .models import SocialLink, Education, Experience, Project, Skill
from .forms import SocialLinkForm, EducationForm, ExperienceForm, ProjectForm, SkillForm


class SocialLinkType(DjangoObjectType):
    class Meta:
        model = SocialLink
        exclude = ("user",)


class EducationType(DjangoObjectType):
    class Meta:
        model = Education
        exclude = ("user",)


class ExperienceType(DjangoObjectType):
    class Meta:
        model = Experience
        exclude = ("user",)


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        exclude = ("user",)


class SkillType(DjangoObjectType):
    class Meta:
        model = Skill
        exclude = ("user",)


class Query(graphene.ObjectType):
    get_social_links = graphene.Field(graphene.List(SocialLinkType), user_id=graphene.Int())
    get_education = graphene.Field(graphene.List(EducationType), user_id=graphene.Int())
    get_experience = graphene.Field(graphene.List(ExperienceType), user_id=graphene.Int())
    get_projects = graphene.Field(graphene.List(ProjectType), user_id=graphene.Int())
    get_skills = graphene.Field(graphene.List(SkillType), user_id=graphene.Int())

    def resolve_get_social_links(self, info, user_id):
        return SocialLink.objects.filter(user=user_id)

    def resolve_get_education(self, info, user_id):
        return Education.objects.filter(user=user_id)

    def resolve_get_experience(self, info, user_id):
        return Experience.objects.filter(user=user_id)

    def resolve_get_projects(self, info, user_id):
        return Project.objects.filter(user=user_id)

    def resolve_get_skills(self, info, user_id):
        return Skill.objects.filter(user=user_id)


class SocialLinkMutation(DjangoModelFormMutation):
    social = graphene.Field(SocialLinkType)

    class Meta:
        form_class = SocialLinkForm


class EducationMutation(DjangoModelFormMutation):
    education = graphene.Field(EducationType)

    class Meta:
        form_class = EducationForm


class ExperienceMutation(DjangoModelFormMutation):
    experience = graphene.Field(ExperienceType)

    class Meta:
        form_class = ExperienceForm


class ProjectMutation(DjangoModelFormMutation):
    project = graphene.Field(ProjectType)

    class Meta:
        form_class = ProjectForm


class SkillMutation(DjangoModelFormMutation):
    skill = graphene.Field(SkillType)

    class Meta:
        form_class = SkillForm


class Mutation(graphene.ObjectType):
    social = SocialLinkMutation.Field()
    education = EducationMutation.Field()
    experience = ExperienceMutation.Field()
    project = ProjectMutation.Field()
    skill = SkillMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
