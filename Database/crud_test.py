from crud import *


create_category(
    id=1,
    name="aaa",
    description="uuu"
)
create_artwork(
    id=11,
    title="abc",
    description="abc",
    poster_url="abc",
    release_date=date(2020, 12, 12),
    category_id=1,
    age_rating="G",
    star_rating=4.3
)
create_user(
    id=22,
    login="dada",
    password="1234",
    email="qwerty@gmail.com",
    created_at=date(2020, 12, 12)
)
create_comment(
    id=33,
    text="qwertyui",
    likes=33,
    dislikes=2,
    user_id=22,
    artwork_id=11
)
create_tag(
    id=88,
    name="fantasy",
    description="deep dark fantasy"
)
create_review(
    id=66,
    text="dsmods",
    score=2.4,
    user_id=22,
    artwork_id=11
)
