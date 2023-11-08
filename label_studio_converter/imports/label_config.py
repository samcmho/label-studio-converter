from label_studio_converter.imports.colors import COLORS


LABELS = """
  <{# TAG_NAME #} name="{# FROM_NAME #}" toName="image">
{# LABELS #}  </{# TAG_NAME #}>
"""
POLY_LABELS = """
                        strokeWidth="{# STROKE #}" pointSize="{# POINT #}"
                        opacity="{# OPACITY #}">

{# LABELS #}  </{# TAG_NAME #}>
"""

LABELING_CONFIG = """<View>
  <Image name="{# TO_NAME #}" value="$image"/>
{# BODY #}</View>
"""


def generate_label_config(
    categories, tags, to_name='image', from_name='label', filename=None
):
    labels = ''
    for key in sorted(categories.keys()):
        color = COLORS[int(key) % len(COLORS)]
        label = f'    <Label value="{categories[key]}" background="rgba({color[0]}, {color[1]}, {color[2]}, 1)"/>\n'
        labels += label

    body = ''
    for from_name in [tag_key for tag_key in tags.keys() if type(tags[tag_key]) == str]:
        tag_body = (
            str(LABELS)
            .replace('{# TAG_NAME #}', tags[from_name])
            .replace('{# LABELS #}', labels)
            .replace('{# TO_NAME #}', to_name)
            .replace('{# FROM_NAME #}', from_name)
        ) 
        if tags[from_name] == 'PolygonLabels':
            tag_body = (
                tag_body.split('\n')[:-1] + # All of the current tag, minus the closing bracket
                str(POLY_LABELS)
                .replace('{# STROKE #}', poly_ops['stroke'])
                .replace('{# POINT #}', poly_ops['pointSize'])
                .replace('{# OPACITY #}', poly_ops['opacity'])
            )
        body += f'\n  <Header value="{tags[from_name]}"/>' + tag_body

    config = (
        str(LABELING_CONFIG)
        .replace('{# BODY #}', body)
        .replace('{# TO_NAME #}', to_name)
    )

    if filename:
        with open(filename, 'w') as f:
            f.write(config)

    return config
