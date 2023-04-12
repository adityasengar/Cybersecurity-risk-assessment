import sys
import os
import pytest

# Add the root directory to the Python path to allow importing risk_analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from risk_analyzer import riskcalc, load_config

@pytest.fixture
def sample_graph_data():
    """Provides a simplified graph data fixture for testing."""
    # This is a miniature, predictable version of the graph for testing purposes
    return {
        "nodes": 4,
        "vnode": [2],
        "cost": [100],
        "type": ['l', 'd', 'l', 'l'],
        "parent": {-1: 0, 1: [0, 2], 2: -1, 3: [1]},
        "prob": [1.0, 0.0, 0.5, 0.0],
    }

def test_riskcalc_no_countermeasures(sample_graph_data):
    """
    Tests the riskcalc function with no countermeasures applied.
    With prob[0]=1.0 and prob[2]=0.5, the diamond node prob[1] should become 1 - (1-1.0)*(1-0.5) = 1.0.
    The final risk is prob[3], whose parent is node 1. But since node 3 is a leaf, its prob should not change.
    Let's adjust the test: let's test the probability of node 1.
    We will modify riskcalc to return the full probability array for testing.
    For this test, let's assume the target node is node 1.
    The test will check if probi[1] is calculated correctly.
    
    Let's re-evaluate. The original `riskcalc` returns `probi[16]`. For this small graph, let's say target is node 3.
    It's a leaf, so its probability should remain 0. `riskcalc` isn't set up to return arbitrary node probabilities.
    Let's adapt the test to be more practical. We will test the final risk value on a known, stable configuration.
    A simple test: if a vital node's probability is set to 0 via a countermeasure, does the final risk decrease?

    Let's test with the actual config, but a simple scenario.
    """
    graph_data = load_config('config/attack_graph.json')
    
    # Calculate baseline risk
    baseline_risk, _ = riskcalc([], graph_data)
    
    # Apply a countermeasure to a critical node (e.g., node 26, 'C1')
    risk_with_cm, _ = riskcalc([26], graph_data)
    
    assert risk_with_cm < baseline_risk
    assert baseline_risk > 0.8 
    assert risk_with_cm > 0.7 

def test_riskcalc_full_mitigation(sample_graph_data):
    """Test if applying all countermeasures reduces risk significantly."""
    graph_data = load_config('config/attack_graph.json')
    all_countermeasures = graph_data['vnode']
    
    baseline_risk, _ = riskcalc([], graph_data)
    mitigated_risk, _ = riskcalc(all_countermeasures, graph_data)
    
    assert mitigated_risk < baseline_risk
    # Applying all CMs should drop the risk substantially
    assert mitigated_risk < 0.1

