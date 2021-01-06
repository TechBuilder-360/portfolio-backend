import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import SocialLink, Education, Experience, Project, Skill, SubSkill, Accomplishment


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
        exclude = ("user", "sub_skills")


class SubSkillType(DjangoObjectType):
    class Meta:
        model = SubSkill
        fields = ("id", "skill", "title")


class AccomplishmentType(DjangoObjectType):
    class Meta:
        model = Accomplishment
        exclude = ("user",)


class Query(graphene.ObjectType):
    social = graphene.Field(graphene.List(SocialLinkType), username=graphene.String())
    education = graphene.Field(graphene.List(EducationType), username=graphene.String())
    experience = graphene.Field(graphene.List(ExperienceType), username=graphene.String())
    project = graphene.Field(graphene.List(ProjectType), username=graphene.String())
    skills = graphene.Field(graphene.List(SkillType), username=graphene.String())
    subskill = graphene.Field(graphene.List(SubSkillType), username=graphene.String())
    accomplishment = graphene.Field(graphene.List(AccomplishmentType), username=graphene.String())

    @staticmethod
    def resolve_social(self, info, username):
        return SocialLink.objects.filter(user__username=username)

    @staticmethod
    def resolve_education(self, info, username):
        return Education.objects.filter(user__username=username)

    @staticmethod
    def resolve_experience(self, info, username):
        return Experience.objects.filter(user__username=username)

    @staticmethod
    def resolve_project(self, info, username):
        return Project.objects.filter(user__username=username)

    @staticmethod
    def resolve_skills(self, info, username):
        return Skill.objects.filter(user__username=username)

    @staticmethod
    def resolve_subskill(self, info, username):
        return SubSkill.objects.filter(skill__user__username=username)

    @staticmethod
    def resolve_accomplishment(self, info, username):
        return Accomplishment.objects.filter(user__username=username)


class SocialLinkMutation(graphene.Mutation):
    social = graphene.Field(SocialLinkType)
    created = graphene.Boolean()

    class Arguments:
        url = graphene.String(required=True)
        label = graphene.String(required=True)
        id = graphene.ID()

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        data['id'] = data['id'] or None
        social, created = SocialLink.objects.update_or_create(
            user=user,
            id=data.get('id'),
            defaults=data
        )
        return SocialLinkMutation(created=created, social=social)


class RemoveSocialLink(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, id):
        user = info.context.user
        try:
            SocialLink.objects.get(user=user, id=id).delete()
            return RemoveSocialLink(ok=True)
        except SocialLink.DoesNotExist:
            return RemoveSocialLink(ok=False, warning='Social contact does not exist')


class EducationMutation(graphene.Mutation):
    education = graphene.Field(EducationType)
    created = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)
        institution = graphene.String(required=True)
        start_year = graphene.String(required=True)
        end_year = graphene.String(required=True)
        in_progress = graphene.Boolean(required=False)
        degree = graphene.String(required=True)
        course = graphene.String(required=True)

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        data['id'] = data['id'] or None
        education, created = Education.objects.update_or_create(
            user=user,
            id=data.get('id'),
            defaults=data
        )
        return EducationMutation(created=created, education=education)


class RemoveEducation(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, id):
        user = info.context.user
        try:
            Education.objects.get(user=user, id=id).delete()
            return RemoveEducation(ok=True)
        except Education.DoesNotExist:
            return RemoveEducation(ok=False, message='Education does not exist')


class ExperienceMutation(graphene.Mutation):
    experience = graphene.Field(ExperienceType)
    created = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)
        organization = graphene.String(required=True)
        position = graphene.String(required=True)
        description = graphene.String(required=True)
        in_progress = graphene.Boolean(required=False)
        start_year = graphene.String(required=True)
        end_year = graphene.String(required=True)

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        data['id'] = data['id'] or None
        experience, created = Experience.objects.update_or_create(
            user=user,
            id=data.get('id'),
            defaults=data
        )
        return ExperienceMutation(created=created, experience=experience)


class RemoveExperience(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, id):
        user = info.context.user
        try:
            Experience.objects.get(user=user, id=id).delete()
            return RemoveExperience(ok=True)
        except Experience.DoesNotExist:
            return RemoveExperience(ok=False, message='Experience does not exist')


class ProjectMutation(graphene.Mutation):
    project = graphene.Field(ProjectType)
    created = graphene.Boolean()

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        project_url = graphene.String(required=True)
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        data['id'] = data['id'] or None
        project, created = Project.objects.update_or_create(
            user=user,
            id=data.get('id'),
            defaults=data
        )
        return ProjectMutation(created=created, project=project)


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
    created = graphene.Boolean()

    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        data['id'] = data['id'] or None
        skill, created = Skill.objects.update_or_create(
            user=user,
            id=data.get('id'),
            defaults=data
        )
        return SkillMutation(created=created, skill=skill)


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
            return SkillRemove(ok=True)
        except Skill.DoesNotExist:
            return SkillRemove(ok=False, warning='Skill does not exist')


class SubSkillMutation(graphene.Mutation):
    subSkill = graphene.Field(SubSkillType)
    created = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        title = graphene.String(required=True)
        skill = graphene.Int(required=True)

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        try:
            data['skill'] = Skill.objects.get(id=data.get('skill'), user=user)
            subSkill, created = SubSkill.objects.update_or_create(
                skill=data['skill'],
                title=data.get('title'),
                defaults=data
            )
            return SubSkillMutation(created=created, subSkill=subSkill)
        except Skill.DoesNotExist:
            return SubSkillMutation(warning="Skill does not exist")


class SubSkillRemove(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, id):
        user = info.context.user
        try:
            SubSkill.objects.get(skill__user=user, id=id).delete()
            return SubSkillRemove(ok=True)
        except SubSkill.DoesNotExist:
            return SubSkillRemove(ok=False, warning='Skill does not exist')


class AccomplishmentMutation(graphene.Mutation):
    id = graphene.Int()
    created = graphene.Boolean()

    class Arguments:
        course = graphene.String(required=True)
        certificate = graphene.String(required=True)
        issuer = graphene.String(required=True)
        description = graphene.String(required=False)
        id = graphene.String(required=False)

    @login_required
    def mutate(self, info, **data):
        user = info.context.user
        data['id'] = data.get('id') or None
        accomplishment, created = Accomplishment.objects.update_or_create(
            user=user,
            id=data.get('id'),
            defaults=data
        )
        return AccomplishmentMutation(created=created, id=accomplishment.id)


class AccomplishmentRemove(graphene.Mutation):
    ok = graphene.Boolean()
    warning = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, id):
        user = info.context.user
        try:
            Accomplishment.objects.get(user=user, id=id).delete()
            return AccomplishmentRemove(ok=True)
        except Accomplishment.DoesNotExist:
            return AccomplishmentRemove(ok=False, warning='Accomplishment does not exist')


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
    sub_skill = SubSkillMutation.Field()
    remove_subSkill = SubSkillRemove.Field()
    accomplishment = AccomplishmentMutation.Field()
    remove_accomplishment = AccomplishmentRemove.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
