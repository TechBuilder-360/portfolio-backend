import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphene_django.forms.mutation import DjangoModelFormMutation
from .models import SocialLink, Education, Experience, Project, Skill
from .forms import EducationForm, ExperienceForm


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
    get_social_links = graphene.Field(graphene.List(SocialLinkType), username=graphene.String())
    get_education = graphene.Field(graphene.List(EducationType), username=graphene.String())
    get_experience = graphene.Field(graphene.List(ExperienceType), username=graphene.String())
    get_projects = graphene.Field(graphene.List(ProjectType), username=graphene.String())
    get_skills = graphene.Field(graphene.List(SkillType), username=graphene.String())


    @staticmethod
    def resolve_get_social_links(self, info, username):
        return SocialLink.objects.filter(user__username=username)

    @staticmethod
    def resolve_get_education(self, info, username):
        return Education.objects.filter(user__username=username)

    @staticmethod
    def resolve_get_experience(self, info, username):
        return Experience.objects.filter(user__username=username)

    @staticmethod
    def resolve_get_projects(self, info, username):
        return Project.objects.filter(user__username=username)

    @staticmethod
    def resolve_get_skills(self, info, username):
        return Skill.objects.filter(user__username=username)


class SocialLinkMutation(graphene.Mutation):
    social = graphene.Field(SocialLinkType)
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        url = graphene.String(required=True)
        label = graphene.String(required=True)
        id = graphene.ID()

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        try:
            SocialLink.objects.get(user=user, profile_url=data['url'])
            return SocialLinkMutation(ok=False, warning='Social contact already exist')
        except SocialLink.DoesNotExist:
            social, created = SocialLink.objects.update_or_create(
                user=info.context.user,
                id=data.get('id'),
                defaults=data
            )
        return SocialLinkMutation(ok=True, social=social)


class RemoveSocialLink(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        social_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, social_id):
        user = info.context.user
        try:
            SocialLink.objects.get(user=user, id=social_id).delete()
            return RemoveSocialLink(ok=True)
        except SocialLink.DoesNotExist:
            return RemoveSocialLink(ok=False, warning='Social contact does not exist')


class EducationMutation(DjangoModelFormMutation):
    education = graphene.Field(EducationType)
    education_id = graphene.ID()
    ok = graphene.Boolean()

    class Meta:
        form_class = EducationForm

    @login_required
    def perform_mutate(self, info, education_id=None):
        user = info.context.user
        education, created = Education.objects.update_or_create(
            user=user,
            id=education_id,
            defaults=self.data
        )
        EducationMutation(ok=True, education=education)


class RemoveEducation(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        education_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, education_id):
        user = info.context.user
        try:
            Education.objects.get(user=user, id=education_id).delete()
            return RemoveEducation(ok=True)
        except Education.DoesNotExist:
            return RemoveEducation(ok=False, warning='Education does not exist')


class ExperienceMutation(DjangoModelFormMutation):
    experience = graphene.Field(ExperienceType)
    experience_id = graphene.ID()
    ok = graphene.Boolean()

    class Meta:
        form_class = ExperienceForm

    @login_required
    def perform_mutate(self, info, experience_id=None):
        user = info.context.user
        experience, created = Experience.objects.update_or_create(
            user=user,
            id=experience_id,
            defaults=self.data
        )
        EducationMutation(ok=True, experience=experience)


class RemoveExperience(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        experience_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, experience_id):
        user = info.context.user
        try:
            Experience.objects.get(user=user, id=experience_id).delete()
            return RemoveExperience(ok=True)
        except Experience.DoesNotExist:
            return RemoveExperience(ok=False, warning='Experience does not exist')


class ProjectMutation(graphene.Mutation):
    project = graphene.Field(ProjectType)
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        title = graphene.String(required=True)
        url = graphene.String(required=True)
        id = graphene.ID()

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        try:
            Project.objects.get(user=user, project_url=data['url'])
            return ProjectMutation(ok=False, warning='Project already exist')
        except Project.DoesNotExist:
            project, created = Project.objects.update_or_create(
                user=info.context.user,
                id=data.get('id'),
                defaults=data
            )
        return ProjectMutation(ok=True, project=project)


class RemoveProject(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        project_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, project_id):
        user = info.context.user
        try:
            Project.objects.get(user=user, id=project_id).delete()
            return RemoveProject(ok=True)
        except Project.DoesNotExist:
            return RemoveProject(ok=False, warning='Skill does not exist')


class SkillMutation(graphene.Mutation):
    skill = graphene.Field(SkillType)
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID()

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        try:
            Skill.objects.get(user=user, title=data['title'])
            return SkillMutation(ok=False, warning='Skill already exist')
        except Skill.DoesNotExist:
            skill, created = Skill.objects.update_or_create(
                user=info.context.user,
                id=data.get('id'),
                defaults=data
            )
        return SkillMutation(ok=True, skill=skill)


class SkillRemove(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        skill_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, skill_id):
        user = info.context.user
        try:
            Skill.objects.get(user=user, id=skill_id).delete()
            return SkillMutation(ok=True)
        except Skill.DoesNotExist:
            return SkillMutation(ok=False, warning='Skill does not exist')


class Mutation(graphene.ObjectType):
    social = SocialLinkMutation.Field()
    remove_social = RemoveSocialLink.Field()
    education = EducationMutation.Field()
    remove_education = RemoveEducation.Field()
    experience = ExperienceMutation.Field()
    remove_experience = RemoveExperience.Field()
    project = ProjectMutation.Field()
    remove_project = RemoveProject.Field()
    skill = SkillMutation.Field()
    remove_skill = SkillRemove.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
