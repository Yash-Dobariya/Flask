# from celery import Celery
# from src.story.model import Story
# from database import db


# celery = Celery('tasks', broker='pyamqp://guest@localhost//', backend='redis://localhost')

# @celery.task
# def end_story(id):
#     story = Story.query.filter_by(id=id).first()
#     db.session.delete(story)
#     db.session.commit()
