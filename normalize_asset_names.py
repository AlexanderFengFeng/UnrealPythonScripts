import unreal


ASSET_CLASS_PREFIXES = {
    'StaticMesh': 'SM_',
    'Material': 'M_',
    'AnimSequence': 'AS_',
    'SkeletalMesh': 'SK_',
    'Skeleton': 'SKEL_',
    'PhysicsAsset': 'PHYS_',
}

editor_asset_lib = unreal.EditorAssetLibrary()
editor_util_lib = unreal.EditorUtilityLibrary()
string_lib = unreal.StringLibrary()
system_lib = unreal.SystemLibrary()


def normalize_asset_names(asset_directory: str = '', recursive: bool = False) -> None:
    assets = [system_lib.get_path_name(asset) for asset in editor_util_lib.get_selected_assets()]
    if asset_directory:
        assets.extend(editor_asset_lib.list_assets(asset_directory, recursive, False))
        
    replaced = 0
    for full_asset_name in assets:
        if normalize_asset_name(full_asset_name):
            replaced += 1
    unreal.log(f'Edited {replaced} names')


def normalize_asset_name(full_asset_name: str) -> bool:
    asset_data = editor_asset_lib.find_asset_data(full_asset_name)
    asset_class = str(asset_data.asset_class)
    asset_name = str(asset_data.asset_name)
    if asset_class not in ASSET_CLASS_PREFIXES:
        unreal.log(f'{asset_class} not accounted for. Add it to the dictionary')

    prefix = ASSET_CLASS_PREFIXES[asset_class]
    if asset_name.startswith(prefix):
        unreal.log(f'{asset_name} already normalized')
        return False
    new_asset_name = ASSET_CLASS_PREFIXES[asset_class] + _format_to_camelcase(asset_name)
    replaced_name = string_lib.replace(full_asset_name, asset_name, new_asset_name)
    editor_asset_lib.rename_asset(full_asset_name, replaced_name)
    unreal.log(f'Replaced: {asset_name} -> {new_asset_name}')
    return True


def _format_to_camelcase(name: str) -> str:
    """Formats snakecased strings to camelcase (does not work with hyphens)."""
    parts = name.split('_')
    for i in range(len(parts)):
        parts[i] = parts[i][0].upper() + parts[i][1:]
    return ''.join(parts)


# Reassign asset_directory to add a directory.
asset_directory = ''  # /Game/DirectoryInContent/PotentialSubdirectory
recursive = False
normalize_asset_names(asset_directory, recursive)