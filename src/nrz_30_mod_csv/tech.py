from gdsfactory.technology import LayerLevel, LayerMap, LayerStack, LogicalLayer
from gdsfactory.typings import Layer

nm = 1e-3


class LAYER(LayerMap):
    # Source: cornerstone-community/Si_220nm_active/process_overview.yaml
    WG: Layer = (3, 0)  # Si etch 2 (120 nm), light field: drawn = protected
    WG_DF: Layer = (4, 0)  # Si etch 2, dark field: drawn = etched
    SLAB: Layer = (5, 0)  # Si etch 3 (100 nm to BOX), drawn = slab kept
    GRA: Layer = (6, 0)  # Si etch 1 (70 nm), grating couplers
    P: Layer = (7, 0)  # 5.7e17 cm^-3
    N: Layer = (8, 0)  # 1.1e18 cm^-3
    PPP: Layer = (9, 0)  # 1e20 cm^-3
    NPP: Layer = (11, 0)  # 1e20 cm^-3
    VIA: Layer = (12, 0)
    METAL: Layer = (13, 0)  # Al electrode, also heaters
    FLOORPLAN: Layer = (99, 0)
    LABEL: Layer = (100, 0)

# Nominal thickness given by foundry, in nm. The actual thickness may vary depending on the process and the specific wafer.
t_box = 2.0
t_si = 220 * nm
t_slab = 100 * nm
t_gra = 150 * nm  # 220 - 70 nm etch
t_tox = 1.0
t_metal = 1.6

LAYER_STACK = LayerStack(
    layers=dict(
        box=LayerLevel(
            layer=LogicalLayer(layer=LAYER.FLOORPLAN),
            thickness=t_box,
            zmin=-t_box,
            material="sio2",
        ),
        core=LayerLevel(
            layer=LogicalLayer(layer=LAYER.WG) - LogicalLayer(layer=LAYER.GRA),
            derived_layer=LogicalLayer(layer=LAYER.WG),
            thickness=t_si,
            zmin=0.0,
            material="si",
            mesh_order=1,
        ),
        grating=LayerLevel(
            layer=LogicalLayer(layer=LAYER.WG) & LogicalLayer(layer=LAYER.GRA),
            derived_layer=LogicalLayer(layer=LAYER.GRA),
            thickness=t_gra,
            zmin=0.0,
            material="si",
            mesh_order=1,
        ),
        slab=LayerLevel(
            layer=LogicalLayer(layer=LAYER.SLAB),
            thickness=t_slab,
            zmin=0.0,
            material="si",
            mesh_order=2,
        ),
        clad=LayerLevel(
            layer=LogicalLayer(layer=LAYER.FLOORPLAN),
            thickness=t_si + t_tox,
            zmin=0.0,
            material="sio2",
            mesh_order=10,
        ),
        metal=LayerLevel(
            layer=LogicalLayer(layer=LAYER.METAL),
            thickness=t_metal,
            zmin=t_si + t_tox,
            material="Aluminum",
            mesh_order=3,
        ),
    )
)