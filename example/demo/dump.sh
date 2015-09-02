python manage.py dumpdata --indent 4 --format json -v 2 \
    sites.site \
    auth.user \
    taggit.tag \
    taggit.taggeditems \
    blognajd.story \
    blognajd.sitesettings \
    inline_media.pictureset \
    inline_media.picture \
    django_comments.comment \
    django_comments_xtd.xtdcomment \
    flatblocks_xtd.flatblockxtd > initdata.json
