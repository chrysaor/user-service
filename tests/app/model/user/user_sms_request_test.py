from app.model.user.user_sms_request import UserSmsRequest


def test_user_sms_request(session):
    assert session is not None

    # Create
    user_sms_req = UserSmsRequest(
        id=1,
        request_id='testrequest_id',
        auth_code='019392',
        sms_type='REGISTER',
        mobile_num='01021290054',
    )

    session.add(user_sms_req)
    session.commit()

    assert user_sms_req is not None

    # Read
    read_user_sms_req = session.query(UserSmsRequest).filter(
        UserSmsRequest.id == 1
    ).first()
    assert read_user_sms_req is not None
    assert read_user_sms_req.sms_type == 'REGISTER'

    # Update
    sms_type = read_user_sms_req.sms_type
    user_sms_req.sms_type = 'LOGIN'
    session.commit()

    read_user_sms_req = session.query(UserSmsRequest).filter(
        UserSmsRequest.id == 1
    ).first()
    assert sms_type != read_user_sms_req.sms_type

    # Delete
    session.delete(read_user_sms_req)
    session.commit()

    read_user_req = session.query(UserSmsRequest).filter(
        UserSmsRequest.id == 1
    ).first()
    assert read_user_req is None
