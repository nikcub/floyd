#!/usr/bin/env python

"""Floyd models
"""

import floyd.db

# @TODO implement field types

class Post(floyd.db.Model):
  stub = ""
  title = ""
  post_type = ""
  post_status = "draft"
  disqus_comments = True
