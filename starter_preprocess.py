"""
starter_preprocess.py
Starter code for text preprocessing - focus on the statistics, not the regex!

This is the same code you'll use in the main Shannon assignment next week.
"""

import re
import json
import requests
from typing import List, Dict, Tuple
from collections import Counter


class TextPreprocessor:
    """Handles all the annoying text cleaning so you can focus on fun stuff"""

    def __init__(self):
        # Gutenberg markers (these are common, add more if needed)
        self.gutenberg_markers = [
            "*** START OF THIS PROJECT GUTENBERG",
            "*** END OF THIS PROJECT GUTENBERG",
            "*** START OF THE PROJECT GUTENBERG",
            "*** END OF THE PROJECT GUTENBERG",
            "*END*THE SMALL PRINT",
            "<<THIS ELECTRONIC VERSION"
        ]

    def clean_gutenberg_text(self, raw_text: str) -> str:
        """Remove Project Gutenberg headers/footers"""
        lines = raw_text.split('\n')

        # Find start and end markers
        start_idx = 0
        end_idx = len(lines)

        for i, line in enumerate(lines):
            # Break the long line into a variable to follow PEP 8
            is_marker = any(
                m in line for m in self.gutenberg_markers[:4]
            )

            if is_marker:
                if "START" in line.upper():
                    start_idx = i + 1
                elif "END" in line.upper():
                    end_idx = i
                    break

        # Join the cleaned lines
        cleaned = '\n'.join(lines[start_idx:end_idx])

        # Remove excessive whitespace
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        cleaned = re.sub(r' {2,}', ' ', cleaned)

        return cleaned.strip()

    def normalize_text(
            self, text: str, preserve_sentences: bool = True
    ) -> str:
        """
        Normalize text while preserving sentence boundaries

        Args:
            text: Input text
            preserve_sentences: If True, keeps . ! ? for sentence detection
        """
        # Convert to lowercase
        text = text.lower()

        # Standardize quotes and dashes
        text = re.sub(r'[\u201c\u201d]', '"', text)
        text = re.sub(r'[\u2018\u2019]', "'", text)
        text = re.sub(r'—|-', '-', text)

        if preserve_sentences:
            # Keep sentence endings but remove other punctuation
            # This regex keeps . ! ? but removes , ; : etc
            text = re.sub(r'[^\w\s.!?\'-]', ' ', text)
        else:
            # Remove all punctuation except apostrophes in contractions
            text = re.sub(r"(?<!\w)'(?!\w)|[^\w\s]", ' ', text)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def tokenize_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def tokenize_words(self, text: str) -> List[str]:
        """Split text into words"""
        # Find all sequences of alphanumeric characters
        return re.findall(r'\b\w+\b', text)

    def tokenize_chars(
        self, text: str, include_space: bool = True
    ) -> List[str]:
        """Split text into characters"""
        if include_space:
            # Replace multiple spaces with single space
            text = re.sub(r'\s+', ' ', text)
            return list(text)
        else:
            return [c for c in text if c != ' ']

    def get_sentence_lengths(self, sentences: List[str]) -> List[int]:
        """Get word count for each sentence"""
        return [len(self.tokenize_words(sent)) for sent in sentences]

    # TODO: Implement these methods for the warm-up assignment

    def fetch_from_url(self, url: str) -> str:
        """
        TODO: Fetch text content from a URL (especially Project Gutenberg)

        Args:
            url: URL to a .txt file

        Returns:
            Raw text content

        Raises:
            Exception if URL is invalid or cannot be reached
        """

        if not url.strip().endswith('.txt'):
            raise ValueError("Invalid URL: Must point to a .txt file")

        try:
            # User-Agent helps avoid 'Connection reset by peer' errors.
            # We break the string into two lines to follow PEP 8 rules.
            headers = {
                'User-Agent': (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            }

            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response.text

        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")

        # Hint: Use requests.get() and validate that it's a .txt URL
        # Don't forget error handling!

    def get_text_statistics(self, text: str) -> Dict:
        """
        TODO: Calculate basic statistics about the text

        Returns dictionary with:
            - total_characters
            - total_words
            - total_sentences
            - avg_word_length
            - avg_sentence_length
            - most_common_words (top 10)
        """
        words = self.tokenize_words(text)
        sentences = self.tokenize_sentences(text)

        total_characters = len(text)
        total_words = len(words)
        total_sentences = len(sentences)

        # Calculate averages with PEP 8 line length fixes
        avg_word_length = (
            sum(len(w) for w in words) / total_words if total_words > 0 else 0
        )
        avg_sentence_length = (
            total_words / total_sentences if total_sentences > 0 else 0
        )

        # USE COUNTER (as per the hint)
        # We lowercase the words here so "The" and "the" are counted together
        word_counts = Counter(w.lower() for w in words)
        most_common_words = dict(word_counts.most_common(10))

        return {
            "total_characters": total_characters,
            "total_words": total_words,
            "total_sentences": total_sentences,
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "most_common_words": most_common_words
        }
        # Hint: Use the existing tokenize methods and Counter

    def create_summary(self, text: str, num_sentences: int = 3) -> str:
        """
        TODO: Create a simple extractive summary by returning the first N sente

        Args:
            text: Cleaned text
            num_sentences: Number of sentences to include

        Returns:
            Summary string
        """

        sentences = self.tokenize_sentences(text)
        # Get the first N sentences
        summary_list = sentences[:num_sentences]
        # Join the first N sentences with a space and return
        return " ".join(summary_list)
        # Hint: Use tokenize_sentences() and join the first N sentences


class FrequencyAnalyzer:
    """Calculate n-gram frequencies from tokenized text"""

    def calculate_ngrams(
        self, tokens: List[str], n: int
    ) -> Dict[Tuple[str, ...], int]:
        """
        Calculate n-gram frequencies

        Args:
            tokens: List of tokens (words or characters)
            n: Size of n-gram (1=unigram, 2=bigram, 3=trigram)

        Returns:
            Dictionary mapping n-grams to their counts
        """
        if n == 1:
            # Special case for unigrams (return as single strings, not tuples)
            return dict(Counter(tokens))

        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i + n])
            ngrams.append(ngram)

        return dict(Counter(ngrams))

    def calculate_probabilities(
        self, ngram_counts: Dict, smoothing: float = 0.0
    ) -> Dict:
        """
        Convert counts to probabilities

        Args:
            ngram_counts: Dictionary of n-gram counts
            smoothing: Laplace smoothing parameter (0 = no smoothing)
        """
        total = sum(ngram_counts.values()) + smoothing * len(ngram_counts)

        probabilities = {}
        for ngram, count in ngram_counts.items():
            probabilities[ngram] = (count + smoothing) / total

        return probabilities

    def save_frequencies(self, frequencies: Dict, filename: str):
        """Save frequency dictionary to JSON file"""
        # Convert tuples to strings for JSON serialization
        json_friendly = {}
        for key, value in frequencies.items():
            if isinstance(key, tuple):
                json_friendly['||'.join(key)] = value
            else:
                json_friendly[key] = value

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_friendly, f, indent=2, ensure_ascii=False)

    def load_frequencies(self, filename: str) -> Dict:
        """Load frequency dictionary from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Convert string keys back to tuples where needed
        frequencies = {}
        for key, value in json_data.items():
            if '||' in key:
                frequencies[tuple(key.split('||'))] = value
            else:
                frequencies[key] = value

        return frequencies


# Example usage to test your setup
if __name__ == "__main__":
    # Test with a small example
    sample_text = """
    This is a test. This is only a test!
    If this were a real emergency, you would be informed.
    """

    preprocessor = TextPreprocessor()
    analyzer = FrequencyAnalyzer()

    # Clean and normalize
    clean_text = preprocessor.normalize_text(sample_text)
    print(f"Cleaned text: {clean_text}\n")

    # Get sentences
    sentences = preprocessor.tokenize_sentences(clean_text)
    print(f"Sentences: {sentences}\n")

    # Get words
    words = preprocessor.tokenize_words(clean_text)
    print(f"Words: {words}\n")

    # Calculate bigrams
    bigrams = analyzer.calculate_ngrams(words, 2)
    print(f"Word bigrams: {bigrams}\n")

    # Calculate character trigrams
    chars = preprocessor.tokenize_chars(clean_text)
    char_trigrams = analyzer.calculate_ngrams(chars, 3)
    top_5_trigrams = dict(list(char_trigrams.items())[:5])
    print(f"Character trigrams (first 5): {top_5_trigrams}")

    print("\n✅ Basic functionality working!")
    print("Now implement the TODO methods for your assignment!")
