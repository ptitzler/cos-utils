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

import argparse
import glob
import os
import sys

from pathlib import Path

from utils.cos import COSWrapper, COSWrapperError


def do_upload(bucket,
              source_spec,
              access_key_id,
              secret_access_key,
              prefix=None,
              wipe=False,
              squash=False,
              recursive=False,
              verbose=False):

    if not access_key_id:
        raise ValueError('access_key_id is required')

    if not secret_access_key:
        raise ValueError('access_key_id is required')

    try:
        # instantiate Cloud Object Storage wrapper
        cw = COSWrapper(access_key_id,
                        secret_access_key)
    except COSWrapperError as cwe:
        print('Error. Cannot access Cloud Object Storage: {}'.format(cwe))
        sys.exit(1)

    # remove all objects from the specified bucket
    try:
        if wipe:
            if verbose:
                print('Clearing bucket "{}" ...'.format(bucket))
            cw.clear_bucket(bucket)
    except Exception as ex:
        print('Error. Clearing of bucket "{}" failed: {}'
              .format(bucket, ex))
        sys.exit(1)

    # upload source
    try:
        if os.path.isdir(source_spec):
            base_dir = source_spec.rstrip(os.path.sep)

            if recursive:
                pattern = '**/*'
            else:
                pattern = '*'

            for file in Path(base_dir).glob(pattern):
                file = str(file)
                if os.path.isdir(file):
                    continue

                if squash:
                    # remove directory offset information
                    key = os.path.basename(file[len(base_dir):])
                else:
                    key = file[len(base_dir)+1:]

                if prefix:
                    # add key name prefix
                    key = '{}/{}'.format(prefix.rstrip('/'), key)

                if verbose:
                    print('Uploading "{}" => "{}"'.format(file, key))

                # upload object to Cloud Object Storage
                cw.upload_object(file,
                                 bucket,
                                 key)
            return

        base_dir = os.path.dirname(source_spec)
        if recursive:
            source_spec = '{}/**/{}'.format(base_dir,
                                            os.path.basename(source_spec))

        for file in glob.iglob(source_spec,
                               recursive=True):
            if os.path.isdir(file):
                # cannot upload a directory
                continue

            if squash:
                # remove directory offset information
                key = os.path.basename(file[len(base_dir):])
            else:
                key = file[len(base_dir)+1:]

            if prefix:
                # add key name prefix
                key = '{}/{}'.format(prefix.rstrip('/'), key)

            if verbose:
                print('Uploading "{}" => "{}"'.format(file, key))

            # upload object to Cloud Object Storage
            cw.upload_object(file,
                             bucket,
                             key)
    except Exception as ex:
        print('Error. Upload to bucket "{}" failed: {}'
              .format(bucket, ex))
        sys.exit(1)


parser = argparse.ArgumentParser(description='Upload files to a Cloud Object '
                                             'Storage bucket')
parser.add_argument('bucket',
                    help='Bucket name')
parser.add_argument('source',
                    help='File or directory')
parser.add_argument('-p',
                    '--prefix',
                    help='Key name prefix')
parser.add_argument('-r',
                    '--recursive',
                    help='Include files in subdirectories',
                    action='store_true')
parser.add_argument('-s',
                    '--squash',
                    help='Exclude subdirectory name from key name',
                    action='store_true')
parser.add_argument('-w',
                    '--wipe',
                    help='Clear bucket prior to upload',
                    action='store_true')

# parse command line parameters
args = parser.parse_args()

# perform upload
do_upload(args.bucket,
          args.source,
          os.environ.get('AWS_ACCESS_KEY_ID'),
          os.environ.get('AWS_SECRET_ACCESS_KEY'),
          args.prefix,
          args.wipe,
          args.squash,
          args.recursive,
          verbose=True)
