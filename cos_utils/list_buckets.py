#!/usr/bin/env python
#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# This utility lists the content of an existing bucket in
# a Cloud Object Storage instance on IBM Cloud.
#


import argparse
import os
import re
import sys

from .cos import COSWrapper, COSWrapperError


class ListError(Exception):
    pass


def do_list(access_key_id,
            secret_access_key,
            pattern=None,
            verbose=False):
    """
    List buckets in selected Cloud Object Storage instance.

    :param access_key_id: HMAC access key id
    :type access_key_id: str
    :param secret_access_key: HMAC secret access key
    :type secret_access_key: str
    :param pattern: bucket name pattern to be applied, defaults to None
    :type pattern: str, optional
    :param verbose: print output to console, defaults to False
    :type verbose: bool, optional
    :return: Objects in bucket matching the pattern
    :rtype: list
    :raises ValueError: A required parameter value is missing.
    :raises ListError: Listing failed due to the specified reason.
    """

    if not access_key_id:
        raise ValueError('Parameter "access_key_id" is required')

    if not secret_access_key:
        raise ValueError('Parameter "secret_access_key" is required')

    try:
        # instantiate Cloud Object Storage wrapper
        cw = COSWrapper(access_key_id,
                        secret_access_key)
    except COSWrapperError as cwe:
        raise ListError('Cannot access Cloud Object Storage: {}'
                        .format(cwe))

    # fetch bucket list
    try:
        bucket_list = cw.get_bucket_list()
        if not pattern:
            return bucket_list

        # sanitize bucket name pattern
        pattern = pattern.replace('*', '.*')
        pattern = pattern.replace('?', '.?')
        pattern = '^{}$'.format(pattern)
        # precompile pattern
        prog = re.compile(pattern)
        return list(filter(prog.match, bucket_list))

    except Exception as ex:
        # catch and mask exception
        raise ListError('Bucket listing failed: {}'
                        .format(ex))


def main():

    epilog_msg = 'Environment variables AWS_ACCESS_KEY_ID and ' \
                 'AWS_SECRET_ACCESS_KEY must be defined to run the utility.'

    parser = argparse.ArgumentParser(description='List buckets in '
                                                 'Cloud Object '
                                                 'Storage instance.',
                                     epilog=epilog_msg)

    parser.add_argument('pattern',
                        help='Bucket name spec (supported wildcards: * and ?)')

    # parse command line parameters
    args = parser.parse_args()

    # verify that the required environment variables are set
    # - AWS_ACCESS_KEY_ID
    # - AWS_SECRET_ACCESS_KEY
    if (os.environ.get('AWS_ACCESS_KEY_ID') is None) or \
       (os.environ.get('AWS_SECRET_ACCESS_KEY') is None):
        print('Error. Environment variables AWS_ACCESS_KEY_ID'
              ' and AWS_SECRET_ACCESS_KEY must be set.')
        sys.exit(1)

    try:
        # fetch bucket list
        bucket_list = do_list(os.environ['AWS_ACCESS_KEY_ID'],
                              os.environ['AWS_SECRET_ACCESS_KEY'],
                              args.pattern,
                              verbose=True)

        # display sorted bucket list
        if bucket_list:
            for bucket in sorted(bucket_list):
                print(bucket)

        print('The Cloud Object Storage instance contains {} '
              'bucket(s) matching "{}".'
              .format(len(bucket_list), args.pattern))
    except Exception as ex:
        print('Error. {}'.format(ex))
        # exit with non-zero return code
        sys.exit(1)


if __name__ == '__main__':
    main()
