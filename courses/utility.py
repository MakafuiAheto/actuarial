import enum


class AreaOfSpecialization(enum.Enum):
    LIFE = ("LI", "Life Insurance")
    GENERAL = ("GI", "General Insurance")
    PENSION = ("PEN", "Pensions")
    HEALTH = ("HI", "Health Insurance")

    def __init__(self, title, industry):
        self.title = title
        self.industry = industry


class Gender(enum.Enum):
    MALE = ("M", "Male")
    FEMALE = ("F", "Female")

    def __init__(self, title, gender):
        self.title = title
        self.gender = gender


class Permissions(enum.Enum):
    # author permissions
    create_author = ("create_new_author", "create_new_author")
    edit_author = ("edit_author", "edit_author")
    get_authors = ("get_all_authors", "get_all_authors")
    delete_author = ("delete_author_details", "delete_author_details")
    delete_authors = ("delete_authors", "delete_authors")

    # video permissions
    create_video = ("create_new_video", "create_new_video")
    delete_video = ("delete_video", "delete_video")
    edit_video = ("edit_video", "edit_video")
    get_videos = ("get_videos", "get_videos")

    # comment permissions
    create_comment = ("create_new_comment", "create_new_comment")
    edit_comment = ("edit_comment", "edit_comment")
    delete_comment = ("delete_comment", "delete_comment")
    get_comments = ("get_all_videos", "get_all_videos")
    get_comment = ("get_comment", "get_comment")
    delete_comments = ("delete_all_comments", "delete_all_comments")

    def __init__(self, key, result):
        self.key = key
        self.result = result


class AuthorPermissionExceptions(enum.Enum):
    delete_authors = Permissions.delete_authors


class StudentPermissionExceptions(enum.Enum):
    create_author = Permissions.create_author
    edit_author = Permissions.edit_author
    delete_authors = Permissions.delete_authors
    delete_author = Permissions.delete_author
    create_video = Permissions.create_video
    delete_video = Permissions.delete_video
    edit_video = Permissions.edit_video
    delete_comments = Permissions.delete_comments
