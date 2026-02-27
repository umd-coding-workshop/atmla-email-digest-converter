import unittest

from email_convert import decode_filename


class TestDecodeFilename(unittest.TestCase):
    def test_plain_filename_is_unchanged(self):
        """Non-encoded filenames should be returned as-is."""
        input_name = "report.pdf"
        expected = "report.pdf"
        self.assertEqual(decode_filename(input_name), expected)

    def test_rfc2047_iso_8859_1_q_encoded_filename(self):
        """
        RFC 2047 Q-encoded filename:
        =?iso-8859-1?Q?HIDDENWEBannouncement.doc?=
        should decode to: HIDDENWEBannouncement.doc
        """
        encoded = "=?iso-8859-1?Q?HIDDENWEBannouncement.doc?="
        expected = "HIDDENWEBannouncement.doc"
        self.assertEqual(decode_filename(encoded), expected)

    def test_whitespace_is_stripped(self):
        """Leading/trailing whitespace should not affect decoding."""
        encoded = "  =?iso-8859-1?Q?HIDDENWEBannouncement.doc?=  "
        expected = "HIDDENWEBannouncement.doc"
        self.assertEqual(decode_filename(encoded), expected)

    def test_empty_string_is_handled(self):
        """
        When an empty string is provided, decode_filename should return a value of
        the form 'attachment-<UUID>'.
        """
        result = decode_filename("")

        # Basic prefix check
        self.assertTrue(result.startswith("attachment-"))

        # Extract the UUID part after 'attachment-'
        uuid_part = result[len("attachment-"):]

       # UUID4 pattern (version 4, variant 1)
        uuid4_regex = (
            r"^[0-9a-fA-F]{8}-"
            r"[0-9a-fA-F]{4}-"
            r"4[0-9a-fA-F]{3}-"
            r"[89abAB][0-9a-fA-F]{3}-"
            r"[0-9a-fA-F]{12}$"
        )
        self.assertRegex(uuid_part, uuid4_regex)



if __name__ == "__main__":
    unittest.main()
