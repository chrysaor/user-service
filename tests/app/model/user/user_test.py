from app.model.user.user import User


def test_user(session):
    assert session is not None

    # Create
    user_instance = User(
        id=1,
        email='chrysaor@naver.com',
        password=User.get_password('test1234'),
        nickname='Hello',
        name='jaewookim',
        mobile_num='01021290054',
    )

    session.add(user_instance)
    session.commit()

    assert user_instance is not None

    # Read
    read_user = session.query(User).filter(User.id == 1).first()
    assert read_user is not None

    # Update
    email = read_user.email
    read_user.email = 'test@test.com'
    session.commit()

    read_user = session.query(User).filter(User.id == 1).first()
    assert email != read_user.email

    # Delete
    session.delete(read_user)
    session.commit()

    read_user = session.query(User).filter(User.id == 1).first()
    assert read_user is None
