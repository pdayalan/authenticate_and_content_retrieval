#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.install_dependencies")


name = "authenticate_and_content_retrieval"
version = "0.1"
summary = "Simple Web Application"
description = "A simple web application using Flask"
authors = [Author("Anirudh Uppal", "anirudh.uppal@gmail.com")]
url = "https://github.com/anuppal/authenticate_and_content_retrieval"
license = "MIT"

default_task = "publish"


@init
def set_properties(project):
    project.build_depends_on('flask', 'boto3')
