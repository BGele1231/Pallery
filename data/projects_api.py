import flask
import sqlalchemy
from flask import jsonify, make_response, request
from . import db_session
from .projects import Projects

blueprint = flask.Blueprint(
    'projects_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/projects')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(Projects).all()
    return jsonify(
        {
            'projects':
                [item.to_dict(only=('title', 'image_url'))
                 for item in news]
        }
    )


@blueprint.route('/api/projects/<int:projects_id>', methods=['GET'])
def get_one_project(projects_id):
    db_sess = db_session.create_session()
    projects = db_sess.query(Projects).get(projects_id)
    if not projects:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'projects': projects.to_dict(only=(
                'title', 'annotation', 'image_url', 'docs_url', 'authors_users')),
        }
    )


@blueprint.route('/api/projects/<int:projects_id>', methods=['DELETE'])
def delete_project(projects_id):
    db_sess = db_session.create_session()
    projects = db_sess.query(Projects).get(projects_id)
    if not projects:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(projects)
    db_sess.commit()
    return jsonify({'success': 'OK'})