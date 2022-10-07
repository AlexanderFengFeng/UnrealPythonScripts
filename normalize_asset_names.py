import unreal


ASSET_CLASS_PREFIXES = {
    'StaticMesh': 'SM_',
    'Material': 'M_',
    'Animation Sequence': '',
}


def normalize_asset_names(asset_directory: str, recursive: bool = False) -> None:
    editor_asset_lib = unreal.EditorAssetLibrary()
    string_lib = unreal.StringLibrary()

    replaced = 0
    assets = editor_asset_lib.list_assets(asset_directory, recursive, False)
    for full_asset_name in assets:
        asset_data = editor_asset_lib.find_asset_data(full_asset_name)
        asset_class = str(asset_data.asset_class)
        asset_name = str(asset_data.asset_name)
        prefix = ASSET_CLASS_PREFIXES[asset_class]
        if asset_name.startswith(prefix):
            unreal.log(f'{asset_name} already normalized')
            continue

        if asset_class not in ASSET_CLASS_PREFIXES:
            unreal.log(f'{asset_class} not accounted for. Add it to the dictionary')
        else:
            new_asset_name = ASSET_CLASS_PREFIXES[asset_class] + _format_to_camelcase(asset_name)
            replaced_name = string_lib.replace(full_asset_name, asset_name, new_asset_name)
            editor_asset_lib.rename_asset(full_asset_name, replaced_name)
            replaced += 1
            unreal.log(f'Replaced: {asset_name} -> {new_asset_name}')
    unreal.log(f'Edited {replaced} names')


def _format_to_camelcase(name: str) -> str:
    """Formats snakecased strings to camelcase (does not work with hyphens)."""
    parts = name.split('_')
    for i in range(len(parts)):
        parts[i] = parts[i][0].upper() + parts[i][1:]
    return ''.join(parts)

# Uncomment and reassign asset_directory.
# asset_directory = '/Game/DirectoryInContent/PotentialSubdirectory'
recursive = False
normalize_asset_names(asset_directory, recursive)

