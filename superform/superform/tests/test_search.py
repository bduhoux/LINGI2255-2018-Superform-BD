import pytest
import os
import tempfile
from superform import app, db
from superform.models import Authorization, Channel, User, Post, Publishing
from superform.utils import datetime_converter
from superform.search import query_maker


@pytest.fixture
def client():
    app.app_context().push()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def populate_db():
    User.query.delete()
    user = User(id="michouchou", email="ftg@gmail.com", name="f", first_name="tg", admin=False)
    db.session.add(user)
    user = User(id="googleplusmoderator", email="ripinpeace@google.plus", name="Press F", first_name="To pay respect",
                admin=False)
    db.session.add(user)
    user = User(id="mr_inutile69", email="pasdechannel@channel.channel", name="MR", first_name="PS", admin=False)
    db.session.add(user)
    user = User(id="channelwriter", email="lolcemailincroyable@wtf.com", name="Channel", first_name="von LECRIVAIN",
                admin=False)
    db.session.add(user)
    user = User(id="channelmoder", email="mmmcharal@cool.com", name="Channel", first_name="van Moderate", admin=False)
    db.session.add(user)
    user = User(id="admin", email="admin@gmail.com", name="Admin", first_name="van Ze Broek", admin=True)
    db.session.add(user)

    Channel.query.delete()
    channel = Channel(id=1, name="Twitter", module="superform.plugins.Twitter", config="{}")
    db.session.add(channel)
    channel = Channel(id=2, name="GPlus", module="superform.plugins.Gplus", config="{}")
    db.session.add(channel)
    channel = Channel(id=3, name="RSS", module="superform.plugins.RSS", config="{}")
    db.session.add(channel)
    channel = Channel(id=4, name="GMoins", module="superform.plugins.Gmoins", config="{}")
    db.session.add(channel)

    Authorization.query.delete()
    authorization = Authorization(user_id="michouchou", channel_id=1, permission=1)
    db.session.add(authorization)
    authorization = Authorization(user_id="admin", channel_id=3, permission=2)
    db.session.add(authorization)
    authorization = Authorization(user_id="googleplusmoderator", channel_id=2, permission=2)
    db.session.add(authorization)
    authorization = Authorization(user_id="channelwriter", channel_id=4, permission=1)
    db.session.add(authorization)
    authorization = Authorization(user_id="channelmoder", channel_id=1, permission=2)
    db.session.add(authorization)
    authorization = Authorization(user_id="channelmoder", channel_id=3, permission=1)
    db.session.add(authorization)

    Post.query.delete()
    post = Post(id=1, user_id="channelmoder", title="first title",
                description="That know ask case sex ham dear her spot. Weddings followed the all marianne nor whatever settling. Perhaps six prudent several her had offence. Did had way law dinner square tastes. Recommend concealed yet her procuring see consulted depending. Adieus hunted end plenty are his she afraid. Resources agreement contained propriety applauded neglected use yet. ",
                link_url="http://facebook.com/", image_url="pas", date_from=datetime_converter("2018-07-01"),
                date_until=datetime_converter("2018-07-01"))
    db.session.add(post)
    post = Post(id=2, user_id="michouchou", title="second title",
                description="first title Him rendered may attended concerns jennings reserved now. Sympathize did now preference unpleasing mrs few. Mrs for hour game room want are fond dare. For detract charmed add talking age. Shy resolution instrument unreserved man few. She did open find pain some out. If we landlord stanhill mr whatever pleasure supplied concerns so. Exquisite by it admitting cordially september newspaper an. Acceptance middletons am it favourable.",
                link_url="http://twitter.com/", image_url="", date_from=datetime_converter("2018-11-13"),
                date_until=datetime_converter("2018-11-14"))
    db.session.add(post)
    post = Post(id=3, user_id="michouchou", title="third title",
                description="Man request adapted spirits set pressed. Up to denoting subjects sensible feelings it indulged directly. We dwelling elegance do shutters appetite yourself diverted. Our next drew much you with rank. Tore many held age hold rose than our. She literature sentiments any contrasted. Set aware joy sense young now tears china shy. ",
                link_url="http://google.com/", image_url="de", date_from=datetime_converter("2018-11-15"),
                date_until=datetime_converter("2018-11-16"))
    db.session.add(post)
    post = Post(id=4, user_id="channelmoder", title="fourth nottitle",
                description="Man request adapted spirits set pressed. ", link_url="http://google.com/", image_url="",
                date_from=datetime_converter("2018-11-10"), date_until=datetime_converter("2018-11-17"))
    db.session.add(post)
    post = Post(id=5, user_id="michouchou", title="first title",
                description="Not him old music think his found enjoy merry. Listening acuteness dependent at or an. Apartments thoroughly unsatiable terminated sex how themselves. She are ten hours wrong walls stand early. Domestic perceive on an ladyship extended received do. Why jennings our whatever his learning gay perceive.",
                link_url="http://youtube.com/", image_url="recherche", date_from=datetime_converter("2018-11-18"),
                date_until=datetime_converter("2018-11-19"))
    db.session.add(post)
    post = Post(id=7, user_id="channelmoder", title="lorem ipsum",
                description="Add you viewing ten equally believe put. Separate families my on drawings do oh offended strictly elegance. Perceive jointure be mistress by jennings properly. An admiration at he discovered difficulty continuing. We in building removing possible suitable friendly on. ",
                link_url="http://instagram.com/", image_url="{}", date_from=datetime_converter("2018-11-20"),
                date_until=datetime_converter("2018-11-21"))
    db.session.add(post)
    post = Post(id=8, user_id="channelmoder", title="", description="",
                link_url="", image_url="", date_from=datetime_converter("2018-11-22"),
                date_until=datetime_converter("2018-11-23"))
    db.session.add(post)
    post = Post(id=9, user_id="channelwriter",
                title="him men instrument saw",
                description="It prepare is ye nothing blushes up brought. Or as gravity pasture limited evening on. Wicket around beauty say she. Frankness resembled say not new smallness you discovery. Noisier ferrars yet shyness weather ten colonel. Too him himself engaged husband pursuit musical.",
                link_url="http://linkedin.com/", image_url="http://wordpress.com/",
                date_from=datetime_converter("2018-11-24"), date_until=datetime_converter("2018-11-25"))
    db.session.add(post)
    post = Post(id=10, user_id="channelwriter", title="men instrument",
                description="", link_url="", image_url="", date_from=datetime_converter("2018-11-26"),
                date_until=datetime_converter("2018-11-27"))
    db.session.add(post)
    post = Post(id=11, user_id="channelwriter", title="",
                description="Him rendered may attended concerns jennings reserved now. Sympathize did now preference unpleasing mrs few. Mrs for hour game room want are fond dare. For detract charmed add talking age. Shy resolution instrument unreserved man few. She did open find pain some out. ",
                link_url="http://wordpress.com/", image_url="sur", date_from=datetime_converter("2018-11-28"),
                date_until=datetime_converter("2018-11-29"))
    db.session.add(post)

    Publishing.query.delete()
    publishing = Publishing(post_id=1, channel_id=1, state=0, title="first title",
                            description="That know ask case sex ham dear her spot. Weddings followed the all marianne nor whatever settling. Perhaps six prudent several her had offence. Did had way law dinner square tastes. Recommend concealed yet her procuring see consulted depending. Adieus hunted end plenty are his she afraid. Resources agreement contained propriety applauded neglected use yet. ",
                            link_url="http://facebook.com/", image_url="pas",
                            date_from=datetime_converter("2018-11-11"),
                            date_until=datetime_converter("2018-11-12"), extra="{}")
    db.session.add(publishing)
    publishing = Publishing(post_id=2, channel_id=1, state=1, title="second title",
                            description="first title Him rendered may attended concerns jennings reserved now. Sympathize did now preference unpleasing mrs few. Mrs for hour game room want are fond dare. For detract charmed add talking age. Shy resolution instrument unreserved man few. She did open find pain some out. If we landlord stanhill mr whatever pleasure supplied concerns so. Exquisite by it admitting cordially september newspaper an. Acceptance middletons am it favourable.",
                            link_url="http://twitter.com/", image_url="", date_from=datetime_converter("2018-11-13"),
                            date_until=datetime_converter("2018-11-14"), extra="{ce champs}")
    db.session.add(publishing)
    publishing = Publishing(post_id=3, channel_id=1, state=2, title="third title",
                            description="Man request adapted spirits set pressed. Up to denoting subjects sensible feelings it indulged directly. We dwelling elegance do shutters appetite yourself diverted. Our next drew much you with rank. Tore many held age hold rose than our. She literature sentiments any contrasted. Set aware joy sense young now tears china shy. ",
                            link_url="http://google.com/", image_url="de", date_from=datetime_converter("2018-11-15"),
                            date_until=datetime_converter("2018-11-16"), extra='{"est sans"}')
    db.session.add(publishing)
    publishing = Publishing(post_id=4, channel_id=1, state=0, title="fourth nottitle",
                            description="Man request adapted spirits set pressed. ", link_url="http://google.com/",
                            image_url="", date_from=datetime_converter("2018-11-10"),
                            date_until=datetime_converter("2018-11-17"), extra="{'importance':mais}")
    db.session.add(publishing)
    publishing = Publishing(post_id=5, channel_id=1, state=1, title="first title",
                            description="Not him old music think his found enjoy merry. Listening acuteness dependent at or an. Apartments thoroughly unsatiable terminated sex how themselves. She are ten hours wrong walls stand early. Domestic perceive on an ladyship extended received do. Why jennings our whatever his learning gay perceive.",
                            link_url="http://youtube.com/", image_url="recherche",
                            date_from=datetime_converter("2018-11-18"), date_until=datetime_converter("2018-11-19"),
                            extra="")
    db.session.add(publishing)
    publishing = Publishing(post_id=1, channel_id=3, state=0, title="lorem ipsum",
                            description="Add you viewing ten equally believe put. Separate families my on drawings do oh offended strictly elegance. Perceive jointure be mistress by jennings properly. An admiration at he discovered difficulty continuing. We in building removing possible suitable friendly on. ",
                            link_url="http://instagram.com/", image_url="{}",
                            date_from=datetime_converter("2018-11-11"),
                            date_until=datetime_converter("2018-11-12"), extra="verifions")
    db.session.add(publishing)
    publishing = Publishing(post_id=7, channel_id=3, state=0, title="", description="", link_url="", image_url="",
                            date_from=datetime_converter("2018-11-20"), date_until=datetime_converter("2018-11-21"),
                            extra="{}")
    db.session.add(publishing)
    publishing = Publishing(post_id=8, channel_id=3, state=0, title="him men instrument saw",
                            description="It prepare is ye nothing blushes up brought. Or as gravity pasture limited evening on. Wicket around beauty say she. Frankness resembled say not new smallness you discovery. Noisier ferrars yet shyness weather ten colonel. Too him himself engaged husband pursuit musical.",
                            link_url="http://linkedin.com/", image_url="http://wordpress.com/",
                            date_from=datetime_converter("2018-11-22"), date_until=datetime_converter("2018-11-23"),
                            extra="{}")
    db.session.add(publishing)
    publishing = Publishing(post_id=4, channel_id=3, state=2, title="men instrument", description="", link_url="",
                            image_url="", date_from=datetime_converter("2018-11-10"),
                            date_until=datetime_converter("2018-11-17"), extra="que ça n'as pas")
    db.session.add(publishing)
    publishing = Publishing(post_id=9, channel_id=4, state=1, title="",
                            description="Him rendered may attended concerns jennings reserved now. Sympathize did now preference unpleasing mrs few. Mrs for hour game room want are fond dare. For detract charmed add talking age. Shy resolution instrument unreserved man few. She did open find pain some out. ",
                            link_url="http://wordpress.com/", image_url="sur",
                            date_from=datetime_converter("2018-11-24"),
                            date_until=datetime_converter("2018-11-25"), extra="[]")
    db.session.add(publishing)
    publishing = Publishing(post_id=10, channel_id=4, state=1, title="explained middleton am",
                            description="Entire any had depend and figure winter. Change stairs and men likely wisdom new happen piqued six. Now taken him timed sex world get. Enjoyed married an feeling delight pursuit as offered. As admire roused length likely played pretty to no. Means had joy miles her merry solid order. ",
                            link_url="http://linkedin.com/", image_url="les images",
                            date_from=datetime_converter("2018-11-26"), date_until=datetime_converter("2018-11-27"),
                            extra="")
    db.session.add(publishing)
    publishing = Publishing(post_id=11, channel_id=4, state=2, title="first title",
                            description="Perhaps far exposed age effects. Now distrusts you her delivered applauded affection out sincerity. As tolerably recommend shameless unfeeling he objection consisted. She although cheerful perceive screened throwing met not eat distance.",
                            link_url="http://youtube.com/", image_url="h", date_from=datetime_converter("2018-11-28"),
                            date_until=datetime_converter("2018-11-29"), extra="'d'influence'")
    db.session.add(publishing)


def empty_db():
    User.query.delete()
    user = User(id="michouchou", email="ftg@gmail.com", name="f", first_name="tg", admin=False)
    db.session.add(user)

    Channel.query.delete()
    Authorization.query.delete()
    Post.query.delete()
    Publishing.query.delete()


def test_admin_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = "first title"
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [1, 5, 11] == [pub.post_id for pub in result]


def test_empty_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 12 == len(result)


def test_by_keyword_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = "title saw middleton"
    filter_parameter["search_by_keyword"] = True
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 8 == len(result)
    assert [1, 2, 3, 4, 5, 8, 10, 11] == [pub.post_id for pub in result]


def test_channels_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = "title"
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 5 == len(result)
    assert [1, 2, 3, 4, 5] == [pub.post_id for pub in result]


def test_states_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = "title"
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 4 == len(result)
    assert [2, 3, 5, 11] == [pub.post_id for pub in result]


def test_content_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = False
    filter_parameter["search_in_content"] = True
    filter_parameter["searched_words"] = "or"
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 7 == len(result)
    assert [1, 2, 3, 5, 8, 9, 10] == [pub.post_id for pub in result]


def test_content_keyword_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = False
    filter_parameter["search_in_content"] = True
    filter_parameter["searched_words"] = "drawings any"
    filter_parameter["search_by_keyword"] = True
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [1, 3, 10] == [pub.post_id for pub in result]


def test_content_title_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = True
    filter_parameter["searched_words"] = "first title"
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 4 == len(result)
    assert [1, 2, 5, 11] == [pub.post_id for pub in result]


def test_content_title_keyboard_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = True
    filter_parameter["searched_words"] = "drawings any middleton saw"
    filter_parameter["search_by_keyword"] = True
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 5 == len(result)
    assert [1, 2, 3, 8, 10] == [pub.post_id for pub in result]


def test_order_title_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [1]
    filter_parameter["states"] = [0, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = "title"
    filter_parameter["search_by_keyword"] = True
    filter_parameter["order_by"] = "title"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [1, 4, 3] == [pub.post_id for pub in result]


def test_order_description_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = True
    filter_parameter["order_by"] = "description"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [10, 9, 11] == [pub.post_id for pub in result]


def test_order_date_from_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "date_from"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [9, 10, 11] == [pub.post_id for pub in result]


def test_order_date_until_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "date_until"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [9, 10, 11] == [pub.post_id for pub in result]


def test_order_desc_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "admin").first()
    filter_parameter["channels"] = [4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "date_until"
    filter_parameter["is_asc"] = False

    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [11, 10, 9] == [pub.post_id for pub in result]


def test_writer_empty_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "mr_inutile69").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 0 == len(result)


def test_writer_basic_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "michouchou").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [2, 3, 5] == [pub.post_id for pub in result]



def test_moderator_empty_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "googleplusmoderator").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 0 == len(result)


def test_writer_basic2_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "channelwriter").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [9, 10, 11] == [pub.post_id for pub in result]


def test_moderator_writer_basic_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "channelmoder").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 9 == len(result)
    assert [1, 1, 2, 3, 4, 4, 5, 7, 8] == [pub.post_id for pub in result]


def test_empty_db_search(client):
    empty_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "michouchou").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True

    result = query_maker(filter_parameter)
    assert 0 == len(result)

def test_time_period_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "michouchou").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True
    filter_parameter["date_from"] = "2017-05-07"
    filter_parameter["date_until"] = "2019-07-07"
    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [2, 3, 5] == [pub.post_id for pub in result]
    filter_parameter["date_from"] = "2020-05-07"
    filter_parameter["date_until"] = "2021-07-07"
    result = query_maker(filter_parameter)
    assert 0 == len(result)
    filter_parameter["date_from"] = "2000-05-07"
    filter_parameter["date_until"] = "2001-07-07"
    result = query_maker(filter_parameter)
    assert 0 == len(result)
    filter_parameter["date_from"] = "2020-05-07"
    filter_parameter["date_until"] = "2017-07-07"
    result = query_maker(filter_parameter)
    assert 0 == len(result)
    filter_parameter["date_from"] = "2018-11-16"
    filter_parameter.pop("date_until", None)
    result = query_maker(filter_parameter)
    assert 1 == len(result)
    assert [5] == [pub.post_id for pub in result]
    filter_parameter.pop("date_from", None)
    filter_parameter["date_until"] = "2018-11-15"
    result = query_maker(filter_parameter)
    assert 1 == len(result)
    assert [2] == [pub.post_id for pub in result]

def test_time_period_search(client):
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "michouchou").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = ""
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True
    filter_parameter["date_from"] = "2017-05-07"
    filter_parameter["date_until"] = "2019-07-07"
    result = query_maker(filter_parameter)
    assert 3 == len(result)
    assert [2, 3, 5] == [pub.post_id for pub in result]
    filter_parameter["date_from"] = "2020-05-07"
    filter_parameter["date_until"] = "2021-07-07"
    result = query_maker(filter_parameter)
    assert 0 == len(result)
    filter_parameter["date_from"] = "2000-05-07"
    filter_parameter["date_until"] = "2001-07-07"
    result = query_maker(filter_parameter)
    assert 0 == len(result)
    filter_parameter["date_from"] = "2020-05-07"
    filter_parameter["date_until"] = "2017-07-07"
    result = query_maker(filter_parameter)
    assert 0 == len(result)
    filter_parameter["date_from"] = "2018-11-16"
    filter_parameter.pop("date_until", None)
    result = query_maker(filter_parameter)
    assert 1 == len(result)
    assert [5] == [pub.post_id for pub in result]
    filter_parameter.pop("date_from", None)
    filter_parameter["date_until"] = "2018-11-15"
    result = query_maker(filter_parameter)
    assert 1 == len(result)
    assert [2] == [pub.post_id for pub in result]

def test_sql_injections(client):
    """
    Check if the search module prevents SQL injections:
        - Get publications from all users instead of only this user's
    :return:
    """
    populate_db()
    filter_parameter = dict()
    filter_parameter["user"] = db.session.query(User).filter(User.id == "michouchou").first()
    filter_parameter["channels"] = [1, 2, 3, 4]
    filter_parameter["states"] = [0, 1, 2]
    filter_parameter["search_in_title"] = True
    filter_parameter["search_in_content"] = False
    filter_parameter["searched_words"] = 'you\'ve been PWn3d by XxxxSUCKERHACKERxxxX" OR 1=1 ;-- '
    filter_parameter["search_by_keyword"] = False
    filter_parameter["order_by"] = "post_id"
    filter_parameter["is_asc"] = True
    result = query_maker(filter_parameter)
    assert 0 == len(result)
