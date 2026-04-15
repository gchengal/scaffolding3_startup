"""
app.py
Flask application template for the warm-up assignment

Students need to implement the API endpoints as specified in the assignment.
"""

from flask import Flask, request, jsonify, render_template
from starter_preprocess import TextPreprocessor

app = Flask(__name__)
preprocessor = TextPreprocessor()


@app.route('/')
def home():
    """Render a simple HTML form for URL input"""
    return render_template('index.html')


@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Text preprocessing service is running"
    })


@app.route('/api/clean', methods=['POST'])
def clean_text():
    """
    TODO: Implement this endpoint for Part 3

    API endpoint that accepts a URL and returns cleaned text

    Expected JSON input:
        {"url": "https://www.gutenberg.org/files/1342/1342-0.txt"}

    Returns JSON:
        {
            "success": true/false,
            "cleaned_text": "...",
            "statistics": {...},
            "summary": "...",
            "error": "..." (if applicable)
        }
    """
    try:
        # TODO: Get JSON data from request
        # TODO: Extract URL from the JSON
        # TODO: Validate URL (should be .txt)
        # TODO: Use preprocessor.fetch_from_url()
        # TODO: Clean the text with preprocessor.clean_gutenberg_text()
        # TODO: Normalize with preprocessor.normalize_text()
        # TODO: Get statistics with preprocessor.get_text_statistics()
        # TODO: Create summary with preprocessor.create_summary()
        # TODO: Return JSON response

        # Get JSON data from request
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({"success": False, "error": "No URL provided"}), 400

        # Extract URL from the JSON
        url = data['url']

        # Validate URL (should be .txt)
        if not url.endswith('.txt'):
            return jsonify({"success":
                            False, "error": "URL must end with .txt"}), 400

        # Use preprocessor methods
        raw_text = preprocessor.fetch_from_url(url)
        cleaned_text = preprocessor.clean_gutenberg_text(raw_text)
        normalized_text = preprocessor.normalize_text(cleaned_text)

        # Get statistics and summary
        stats = preprocessor.get_text_statistics(normalized_text)
        summary = preprocessor.create_summary(normalized_text)

        # Return JSON response
        return jsonify({
            "success": True,
            "cleaned_text": normalized_text,
            "statistics": stats,
            "summary": summary
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

        return jsonify({
            "success": False,
            "error": "Not implemented yet - complete this for Part 3!"
        }), 501

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    TODO: Implement this endpoint for Part 3

    API endpoint that accepts raw text and returns statistics only

    Expected JSON input:
        {"text": "Your raw text here..."}

    Returns JSON:
        {
            "success": true/false,
            "statistics": {...},
            "error": "..." (if applicable)
        }
    """
    try:
        # TODO: Get JSON data from request
        # TODO: Extract text from the JSON
        # TODO: Get statistics with preprocessor.get_text_statistics()
        # TODO: Return JSON response

        # Get JSON data from request
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"success":
                            False, "error": "No text provided"}), 400

        # Extract text from the JSON
        text = data['text']

        # Get statistics
        stats = preprocessor.get_text_statistics(text)

        # Return JSON response
        return jsonify({
            "success": True,
            "statistics": stats
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

        return jsonify({
            "success": False,
            "error": "Not implemented yet - complete this for Part 3!"
        }), 501

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

# Error handlers


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("🚀 Starting Text Preprocessing Web Service...")
    print("📖 Available endpoints:")
    print("   GET  /           - Web interface")
    print("   GET  /health     - Health check")
    print("   POST /api/clean  - Clean text from URL")
    print("   POST /api/analyze - Analyze raw text")
    print()
    print("🌐 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")

    app.run(debug=True, port=5000, host='0.0.0.0')
