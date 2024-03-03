CURRENT_LATENCY_PIPELINE = [
                {
                    '$group': {
                        '_id': None,
                        'averageLatency': {
                            '$avg': '$latency'
                        }
                    }
                },
{
                    '$project': {
                        '_id': 0,
                        'latency': '$averageLatency'
                    }
                }
            ]



CURRENT_ERROR_PIPELINE = [
                {
                    '$match': {
                        'status': 'error'
                    }
                }, {
                    '$group': {
                        '_id': None,
                        'count': {
                            '$sum': 1
                        }
                    }
                }, {
                    '$project': {
                        '_id': 0,
                        'count': '$count'
                    }
                }
            ]

CURRENT_SUCCESS_PIPELINE = [
                {
                    '$match': {
                        'status': 'success'
                    }
                }, {
                    '$group': {
                        '_id': None,
                        'count': {
                            '$sum': 1
                        }
                    }
                }, {
                    '$project': {
                        '_id': 0,
                        'count': '$count'
                    }
                }
            ]



TOTAL_TESTS_BY_MINUTES_PIPELINE = [
    {
        '$group': {
            '_id': {
                'date': {
                    '$dateToString': {
                        'format': '%Y-%m-%d %H:%M:00',
                        'date': '$moment'
                    }
                }
            },
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            'date': '$_id.date',
            'count': '$count',
            '_id': 0
        }
    }, {
        '$sort': {
            'date': 1
        }
    }
]


TOTAL_TESTS_PIPELINE = [
    {
        '$group': {
            '_id': {},
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            'count': '$count',
            '_id': 0
        }
    }
]



TOTAL_ERROR_TESTS_PIPELINE = [
    {
        '$match': {
            'status': 'error'
        }
    }, {
        '$group': {
            '_id': {},
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            'count': '$count',
            '_id': 0
        }
    }
]


TOTAL_SUCCESS_TESTS_PIPELINE = [
    {
        '$match': {
            'status': 'success'
        }
    }, {
        '$group': {
            '_id': {},
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            'count': '$count',
            '_id': 0
        }
    }
]


TOTAL_ERROR_TESTS_BY_MINUTE = [
    {
        '$match': {
            'status': 'error'
        }
    }, {
        '$group': {
            '_id': {
                'date': {
                    '$dateToString': {
                        'format': '%Y-%m-%d %H:%M:00',
                        'date': '$moment'
                    }
                }
            },
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            'date': '$_id.date',
            'count': '$count',
            '_id': 0
        }
    }
]


TOTAL_SUCCESS_TESTS_BY_MINUTE = [
    {
        '$match': {
            'status': 'success'
        }
    }, {
        '$group': {
            '_id': {
                'date': {
                    '$dateToString': {
                        'format': '%Y-%m-%d %H:%M:00',
                        'date': '$moment'
                    }
                }
            },
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            'date': '$_id.date',
            'count': '$count',
            '_id': 0
        }
    }
]

DEVICES_STATS_BY_MINUTE = [
    {
        '$match': {
            'status': 'success'
        }
    }, {
        '$group': {
            '_id': {
                'device': '$host',
                'date': {
                    '$dateToString': {
                        'format': '%Y-%m-%d %H:%M:00',
                        'date': '$moment'
                    }
                },
                'averageLatency': {
                    '$avg': '$latency'
                }
            },
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            'date': '$_id.date',
            'device': '$_id.device',
            'latency': '$_id.averageLatency',
            'count': '$count',
            '_id': 0
        }
    }
]


HISTORY_STATS_PIPELINE = [
    {
        '$facet': {
            'total_tests_by_minutes': TOTAL_TESTS_BY_MINUTES_PIPELINE,
            'total_tests': TOTAL_TESTS_PIPELINE,
            'total_error_tests': TOTAL_ERROR_TESTS_PIPELINE,
            'total_success_tests': TOTAL_SUCCESS_TESTS_PIPELINE,
            'total_error_tests_by_minute': TOTAL_ERROR_TESTS_BY_MINUTE,
            'total_success_tests_by_minute': TOTAL_SUCCESS_TESTS_BY_MINUTE,
            'devices_stats_by_minute': DEVICES_STATS_BY_MINUTE

        }
    }
]

CURRENT_STATS_PIPELINE = [
    {
        '$facet': {
            'current_latency_average': CURRENT_LATENCY_PIPELINE,
            'current_errors': CURRENT_ERROR_PIPELINE,
            'current_success': CURRENT_SUCCESS_PIPELINE

        }
    }
]