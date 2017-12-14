# ВНИМАНИЕ: код для примера! Не нужно его бездумно копировать!
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    abort,
    redirect,
    url_for,
    current_app,
)
from sqlalchemy.exc import SQLAlchemyError

from .models import Entity, db
from .forms import EntityCreateForm
from app.comment.models import Comment

module = Blueprint('entity', __name__, url_prefix ='/entity')


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/', methods=['GET'])
def index():
    entities = None
    try:
        entities = Entity.query.join(Comment).order_by(Entity.id).all()
        db.session.commit()
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('Во время запроса произошла непредвиденная ошибка.', 'danger')
        abort(500)
    return render_template('entity/index.html', object_list=entities)


@module.route('/<int:id>/view/', methods=['GET'])
def view(id):
    entity = None
    try:
        entity = Entity.query.outerjoin(Comment).first_or_404(id)
        db.session.commit()
        if entity is None:
            flash('Нет entity с таким идентификатором', 'danger')
            abort(404)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('Во время запроса произошла непредвиденная ошибка', 'danger')
        abort(500)
    return render_template('entity/view.html', object=image)


@module.route('/create/', methods=['GET', 'POST'])
def create():
    form = EntityCreateForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            entity = Entity(**form.data)
            db_session.add(entity)
            db_session.flush()
            id = entity.id
            db_session.commit()
            flash('Запись была успешно добавлена!', 'success')
            return redirect(url_for('entity.view', id=id))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Произошла непредвиденная ошибка во время запроса к базе данных', 'danger')
    return render_template('entity/create.html', form=form)


# Наивное удаление. Чаще всего, будет сложная логика с правильной обработкой
# зависимых объектов.
@module.route('/<int:id>/remove/', methods=['GET', 'POST'])
def remove(id):
  entity = None
  try:
      entity = Entity.query.get(id)
      if entity is None:
          flash('Нет записи с таким идентификатором', 'danger')
  except SQLAlchemyError as e:
      log_error('Error while querying database', exc_info=e)
      flash('Произошла непредвиденная ошибка во время запроса к базе данных', 'danger')
  finally:
      db_session.commit()
      flash('Запись была успешна удалена!', 'success')
  return redirect(url_for('entity.index'))