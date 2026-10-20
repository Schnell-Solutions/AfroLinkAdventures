from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from destination_cms.models import JournalArticle
from destination_cms.youtube import extract_youtube_video_id, youtube_embed_url


class YouTubeUrlParsingTests(SimpleTestCase):
    def test_standard_and_shortened_urls(self):
        cases = {
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ': 'dQw4w9WgXcQ',
            'https://youtube.com/watch?v=dQw4w9WgXcQ&t=30s': 'dQw4w9WgXcQ',
            'https://youtu.be/dQw4w9WgXcQ': 'dQw4w9WgXcQ',
            'https://youtu.be/dQw4w9WgXcQ?t=12': 'dQw4w9WgXcQ',
            'https://www.youtube.com/embed/dQw4w9WgXcQ': 'dQw4w9WgXcQ',
            'https://www.youtube.com/shorts/dQw4w9WgXcQ': 'dQw4w9WgXcQ',
            'https://m.youtube.com/watch?v=dQw4w9WgXcQ': 'dQw4w9WgXcQ',
            'www.youtube.com/watch?v=dQw4w9WgXcQ': 'dQw4w9WgXcQ',
            'youtu.be/dQw4w9WgXcQ': 'dQw4w9WgXcQ',
        }
        for url, expected in cases.items():
            self.assertEqual(extract_youtube_video_id(url), expected, url)

    def test_invalid_urls_return_none(self):
        for url in (
            '',
            None,
            'https://example.com/watch?v=dQw4w9WgXcQ',
            'https://www.youtube.com/watch?v=short',
            'https://www.youtube.com/playlist?list=PLtest',
            'not a url',
        ):
            self.assertIsNone(extract_youtube_video_id(url), url)

    def test_embed_url_uses_nocookie_host(self):
        self.assertEqual(
            youtube_embed_url('https://youtu.be/dQw4w9WgXcQ'),
            'https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ',
        )
        self.assertIsNone(youtube_embed_url('https://example.com/video'))


class JournalArticleYouTubeValidationTests(TestCase):
    def test_clean_rejects_invalid_youtube_url(self):
        article = JournalArticle(
            title_en='Test',
            slug='youtube-validation-test',
            body_en='Body',
            published_at=timezone.localdate(),
            youtube_url='https://vimeo.com/123456',
        )
        with self.assertRaises(ValidationError) as caught:
            article.full_clean()
        self.assertIn('youtube_url', caught.exception.message_dict)

    def test_embed_helpers_are_safe_when_blank(self):
        article = JournalArticle(
            title_en='Test',
            slug='youtube-blank-test',
            body_en='Body',
            published_at=timezone.localdate(),
            youtube_url='',
        )
        self.assertIsNone(article.get_youtube_video_id())
        self.assertIsNone(article.get_youtube_embed_url())
