import unreal


def replace_in_selected(in_pattern: str, out_pattern: str = '') -> None:
    editor_util_lib = unreal.EditorUtilityLibrary()
    system_lib = unreal.SystemLibrary()
    string_lib = unreal.StringLibrary()

    replaced = 0
    selected_assets = editor_util_lib.get_selected_assets()
    for asset in selected_assets:
        asset_name = system_lib.get_object_name(asset)
        if string_lib.contains(asset_name, in_pattern, use_case=False):
            replaced_name = string_lib.replace(asset_name, in_pattern, out_pattern)
            editor_util_lib.rename_asset(asset, replaced_name)
            replaced += 1
            unreal.log(f'Renaming: {asset_name} -> {replaced_name}')

    unreal.log(f'Edited {replaced} assets')

# Uncomment and reassign in_pattern and (optionally) out_pattern.
# in_pattern = 'character_skeletonKing_character_'
out_pattern = ''
replace_in_selected(in_pattern=in_pattern, out_pattern=out_pattern)

