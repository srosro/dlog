"""XML-RPC methods for Zinnia"""

ZINNIA_XMLRPC_PINGBACK = [('xmlrpc.pingback.pingback_ping',
                           'pingback.ping'),
                          ('xmlrpc.pingback.pingback_extensions_get_pingbacks',
                           'pingback.extensions.getPingbacks'),]

ZINNIA_XMLRPC_METAWEBLOG = [('xmlrpc.metaweblog.get_users_blogs',
                             'blogger.getUsersBlogs'),
                            ('xmlrpc.metaweblog.get_user_info',
                             'blogger.getUserInfo'),
                            ('xmlrpc.metaweblog.delete_post',
                             'blogger.deletePost'),
                            ('xmlrpc.metaweblog.get_recent_posts',
                             'metaWeblog.getRecentPosts'),
                            ('xmlrpc.metaweblog.get_post',
                             'metaWeblog.getPost'),
                            ('xmlrpc.metaweblog.new_post',
                             'metaWeblog.newPost'),
                            ('xmlrpc.metaweblog.edit_post',
                             'metaWeblog.editPost'),
                            ('xmlrpc.metaweblog.new_media_object',
                             'metaWeblog.newMediaObject'),]

ZINNIA_XMLRPC_METHODS = ZINNIA_XMLRPC_PINGBACK + ZINNIA_XMLRPC_METAWEBLOG

