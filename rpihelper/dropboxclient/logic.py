# -*- coding: utf-8 -*-

import sys

from dropbox import client, rest

from flask import current_app

from rpihelper.dropboxclient.decorators import command

__all__ = (
    'Client',
)


class Client(object):
    app_key = current_app.config['DROPBOX_APP_KEY']
    app_sercret = current_app.config['DROPBOX_APP_SECRET']
    app_token = current_app.config['DROPBOX_APP_TOKEN']
    api_client = None

    def __init__(self):
        if self.app_token:
            self.api_client = client.DropboxClient(self.app_token)

    def login(self):
        flow = client.DropboxOAuth2FlowNoRedirect(
            self.app_key, self.app_sercret
        )
        authorize_url = flow.start()
        sys.stdout.write('1. Go to: %s \n' % authorize_url)
        sys.stdout.write('2. Click "Allow" (you might have to log in first).\n')
        sys.stdout.write('3. Copy the authorization code.\n')
        code = input('Enter the authorization code here: ').strip()

        try:
            access_token, user_id = flow.finish(code)
            sys.stdout.write('Add token to config `DROPBOX_APP_TOKEN`: %s' % access_token)
        except rest.ErrorResponse as e:
            sys.stdout.write('Error: %s\n' % e)

    @command(exception_return=[])
    def ls_files(self, path):
        """
        Retrieve filenames from folder.

        Args:
            - ``path``: The path to the folder.

        Returns:
            - List with file names or empty list if files not found.
        """
        return [
            md['path'] for md in self.api_client.metadata(path)['contents']
        ]

    @command(exception_return=None)
    def file(self, path):
        """
        Download a file (with latest revision).

        Args:
            - ``path``: The path to the file to be downloaded.

        Returns:
            - Byte string with file content or `None`.
        """
        return self.api_client.get_file(path).read()

    @command(exception_return=None)
    def rm_file(self, path):
        """
        Delete a file or folder.

        Args:
            - ``path``: The path of the file or folder.

        Returns:
            - A dictionary containing the metadata of the just deleted file or None.
        """
        return self.api_client.file_delete(path)
