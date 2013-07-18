python manage.py dumpdata --indent 4 --format json -v 2 \
    sites.site \
    auth.user \
    blognajd.story \
    inline_media.pictureset \
    inline_media.picture \
    comments.comment \
    django_comments_xtd.xtdcomment \
    flatblocks_xtd.flatblockxtd \
    tagging.tag \
    tagging.taggeditem > initial_data.json
