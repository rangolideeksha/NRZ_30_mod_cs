from nrz_30_mod_csv.tech import LAYER, LAYER_STACK


def test_layers():
    assert tuple(LAYER.WG) == (3, 0)
    assert tuple(LAYER.SLAB) == (5, 0)


def test_stack_thickness():
    t = LAYER_STACK.get_layer_to_thickness()
    assert abs(sum(t.values())) > 0  # stack builds and has levels
