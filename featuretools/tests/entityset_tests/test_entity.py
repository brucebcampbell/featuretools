# -*- coding: utf-8 -*-

import pytest

from ..testing_utils import make_ecommerce_entityset

from featuretools import variable_types


@pytest.fixture
def es():
    return make_ecommerce_entityset()


def test_enforces_variable_id_is_str(es):
    assert variable_types.Categorical("1", es["customers"])
    with pytest.raises(AssertionError):
        variable_types.Categorical(1, es["customers"])


def test_is_index_column(es):
    assert es['cohorts'].index == 'cohort'


def test_eq(es):

    es['log'].id = 'customers'
    es['log'].index = 'notid'
    assert not es['customers'].__eq__(es['log'], deep=True)

    es['log'].index = 'id'
    assert not es['customers'].__eq__(es['log'], deep=True)

    es['log'].time_index = 'signup_date'
    assert not es['customers'].__eq__(es['log'], deep=True)

    es['log'].secondary_time_index = {
        'cancel_date': ['cancel_reason', 'cancel_date']}
    assert not es['customers'].__eq__(es['log'], deep=True)

    es['log'].indexed_by = None
    assert not es['log'].__eq__(es['customers'], deep=True)


def test_parents(es):
    assert set(es['log'].parents) == set(['sessions', 'products'])
    assert es['sessions'].parents == ['customers']
    assert set(es['customers'].parents) == set([u'régions', 'cohorts'])
    assert es[u'régions'].parents == []
    assert es['stores'].parents == [u'régions']


def test_update_data(es):
    # TODO: write test for this method, since it has new functionality
    pass
