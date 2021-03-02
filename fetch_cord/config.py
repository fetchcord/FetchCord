#from __future__ import annotations


try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
import os, copy, json, configparser

from . import resources as fc_resources
from .args import parse_args


args = parse_args()


class ConfigError(Exception):
    pass


def load_config():
    default_config = configparser.ConfigParser()
    with pkg_resources.path(fc_resources, "fetch_cord.conf") as path:
        default_config.read_file(open(path))
        default_config.read(
            ["/etc/fetch_cord.conf", os.path.expanduser("~/fetch_cord.conf")]
        )
        if args.fetchcord_config_path != None:
            default_config.read([args.fetchcord_config_path])
        for item in default_config.items():
            print(item)

        default_config = _parsed_config_to_dict(default_config)
        _validate_config(default_config)

        return default_config


# def load_config():
#     base_config = configparser.ConfigParser()
#     base_config.read(["/etc/fetch_cord.conf"])
#     base_config = _parsed_config_to_dict(base_config)
#     _validate_config(base_config)


# #    try:
#     user_config = configparser.ConfigParser()
#     user_config.read("/etc/fetch_cord.conf")
#     user_config = _parsed_config_to_dict(user_config)
# #    except configparser.ParsingError as e:
# #        print(
# #            "Error parsing config file %s. Falling back to default config %s. Error is : %s",
# #            envs.USER_CONFIG_COPY_PATH, envs.DEFAULT_CONFIG_PATH, str(e))
#     return base_config

#     corrected_config = _validate_config(user_config, fallback_config=base_config)


#     return corrected_config


def _validate_config(config, fallback_config=None):

    folder_path = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(folder_path, "config_schema.json")

    with open(schema_path, "r") as f:
        schema = json.load(f)

    corrected_config = copy.deepcopy(config)

    # Checking if the config file has the required sections and options
    for section in schema.keys():

        if section not in config.keys():
            raise ConfigError("Cannot find header for section [%s]" % section)

        for option in schema[section].keys():

            if option not in config[section].keys():
                raise ConfigError(
                    'Cannot find option "%s" in section [%s]' % (option, section)
                )

            valid, msg = _validate_option(
                schema[section][option], config[section][option]
            )

            if not valid:
                error_msg = (
                    'Config parsing : error in option "%s" in section [%s] : %s'
                    % (option, section, msg)
                )
                if fallback_config is not None:
                    print(error_msg)
                    print(
                        'Falling back to default value "%s"',
                        fallback_config[section][option],
                    )
                    corrected_config[section][option] = fallback_config[section][option]

                else:
                    raise ConfigError(error_msg)

    # Checking if the config file has no unknown section or option
    for section in config.keys():

        if section not in schema.keys():
            print("Config parsing : unknown section [%s]. Ignoring.", section)
            continue

        for option in config[section].keys():
            if option not in schema[section].keys():
                print(
                    'Config parsing : unknown option "%s" in section [%s]. Ignoring.',
                    option,
                    section,
                )
                del corrected_config[section][option]

    return corrected_config


def _parsed_config_to_dict(config):

    config_dict = {}

    for section in config.keys():

        if section == "DEFAULT":
            continue

        config_dict[section] = {}

        for option in config[section].keys():
            config_dict[section][option] = config[section][option]

    return config_dict


def _validate_option(schema_option_info, config_option_value):
    valid = False
    msg = "error"

    parameter_type = schema_option_info[0]

    assert parameter_type in ["multi_words", "single_word", "integer"]

    # Multiple-words parameters
    if parameter_type == "multi_words":
        valid, msg = _validate_multi_words(schema_option_info, config_option_value)

    # Single-word parameters
    elif parameter_type == "single_word":
        valid, msg = _validate_single_word(schema_option_info, config_option_value)

    # Integer parameter
    elif parameter_type == "integer":
        valid, msg = _validate_integer(schema_option_info, config_option_value)

    return valid, msg


def _validate_multi_words(schema_option_info, config_option_value):

    parameter_type, allowed_values, can_be_blank = schema_option_info
    assert parameter_type == "multi_words"

    values = config_option_value.replace(" ", "").split(",")

    if values == [""]:
        if not can_be_blank:
            msg = "at least one parameter required"
            return False, msg

    else:
        for val in values:
            if val not in allowed_values:
                msg = 'invalid value "%s"' % val
                return False, msg

    return True, None


def _validate_single_word(schema_option_info, config_option_value):

    parameter_type, allowed_values, can_be_blank = schema_option_info
    assert parameter_type == "single_word"

    val = config_option_value.replace(" ", "")

    if val == "":
        if not can_be_blank:
            msg = "non-blank value required"
            return False, msg

    else:
        if val not in allowed_values:
            msg = 'invalid value "%s"' % val
            return False, msg

    return True, None


def _validate_integer(schema_option_info, config_option_value):

    parameter_type, can_be_blank = schema_option_info
    assert parameter_type == "integer"

    val = config_option_value.replace(" ", "")

    if val == "":
        if not can_be_blank:
            msg = "non-blank integer value required"
            return False, msg

    else:
        try:
            v = int(val)
            if v <= 0:
                raise ValueError
        except ValueError:
            msg = "non-blank integer value required"
            return False, msg

    return True, None
