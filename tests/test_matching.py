"""
Basic unit tests for the core matching algorithm.
Run with: pytest tests/test_matching.py  (requires an app context)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


def test_calculate_match_basic():
    app = create_app(TestConfig)
    with app.app_context():
        from services.matching import calculate_match
        result = calculate_match(
            student_skills=['Python', 'SQL', 'HTML', 'CSS', 'JavaScript'],
            required_skills=['Python', 'SQL', 'JavaScript', 'React']
        )
        assert result['percentage'] == 75
        assert 'react' in result['missing']
        assert 'python' in result['matched']
        assert result['label'] == 'Good Match'


def test_calculate_match_perfect():
    app = create_app(TestConfig)
    with app.app_context():
        from services.matching import calculate_match
        result = calculate_match(['Python', 'SQL'], ['Python', 'SQL'])
        assert result['percentage'] == 100
        assert result['label'] == 'Excellent Match'
        assert result['missing'] == []


if __name__ == '__main__':
    test_calculate_match_basic()
    test_calculate_match_perfect()
    print('All matching tests passed.')
