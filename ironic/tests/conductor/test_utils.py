# coding=utf-8

# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Tests for Ironic Manager test utils."""

from ironic.tests import base
from ironic.tests.conductor import utils


class UtilsTestCase(base.TestCase):
    def setUp(self):
        super(UtilsTestCase, self).setUp()

    def test_fails_to_load_extension(self):
        self.assertRaises(AttributeError,
                          utils.mock_the_extension_manager,
                          'fake',
                          'bad.namespace')
        self.assertRaises(AttributeError,
                          utils.mock_the_extension_manager,
                          'no-such-driver',
                          'ironic.drivers')

    def test_get_mockable_ext_mgr(self):
        (mgr, ext) = utils.mock_the_extension_manager('fake',
                                                      'ironic.drivers')

        # confirm that stevedore did not scan the actual entrypoints
        self.assertNotEqual(mgr._extension_manager.namespace, 'ironic.drivers')
        # confirm mgr has only one extension
        self.assertEqual(len(mgr._extension_manager.extensions), 1)
        # confirm that we got a reference to the extension in this manager
        self.assertEqual(mgr._extension_manager.extensions[0], ext)
        # confirm that it is the "fake" driver we asked for
        self.assertEqual("%s" % ext.entry_point,
                         "fake = ironic.drivers.fake:FakeDriver")
        # Confirm driver is loaded
        self.assertIn('fake', mgr.names)
