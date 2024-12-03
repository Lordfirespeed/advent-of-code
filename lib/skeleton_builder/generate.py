import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError, UndefinedError

from .environment import create_env
from .has_binary_contents import has_binary_contents
from .utils import work_in

type Context = dict[str, object]


def render_file(
    instance_dir: Path,
    template_file: Path,
    context: Context,
    env: Environment,
) -> None:
    """
    :param instance_dir: Absolute path to the resulting generated template instance.
    :param template_file: Input file to generate the file from. Relative to the root
        template dir.
    :param context: Dict for populating the template's variables.
    :param env: Jinja2 template execution environment.
    """
    instance_file_template = env.from_string(str(template_file))
    instance_file = os.path.join(instance_dir, instance_file_template.render(**context))
    file_name_is_empty = os.path.basename(instance_file) == ""
    if file_name_is_empty:
        raise Exception(f"The resulting file name is empty: {template_file} -> {instance_file}")

    if os.path.exists(instance_file):
        raise Exception(f"The resulting file already exists: {template_file} -> {instance_file}")

    if has_binary_contents(template_file):
        shutil.copyfile(template_file, instance_file)
        shutil.copymode(template_file, instance_file)
        return

    if os.path.islink(template_file):
        raise NotImplemented

    instance_file_contents_template = env.get_template(str(template_file))
    instance_file_contents = instance_file_contents_template.render(**context)

    with open(instance_file, 'w', encoding='utf-8') as instance_file_handle:
        instance_file_handle.write(instance_file_contents)

    # Apply file permissions to output file
    shutil.copymode(template_file, instance_file)


def render_directory(
    instance_dir: Path,
    template_dir: Path,
    context: Context,
    env: Environment,
) -> None:
    """
    :param instance_dir: Absolute path to the resulting generated template instance.
    :param template_dir: Input dir to generate the dir from. Relative to the root
        template dir.
    :param context: Dict for populating the template's variables.
    :param env: Jinja2 template execution environment.
    """
    instance_dir_template = env.from_string(str(template_dir))
    instance_dir = Path(instance_dir, instance_dir_template.render(**context))

    if instance_dir.exists():
        raise Exception(f"The resulting directory already exists: {template_dir} -> {instance_dir}")

    instance_dir.mkdir(parents=True)


def use_template_file(
    instance_file: Path,
    template_file: Path,
    context: Context,
) -> None:
    """
    :param instance_file: Absolute path to the resulting generated template instance.
    :param template_file: Absolute path to the template file.
    :param context: Dict for populating the template's variables.
    """
    raise NotImplemented


def use_template_dir(
    instance_dir: Path,
    template_dir: Path,
    context: Context,
) -> None:
    """
    :param instance_dir: Absolute path to the resulting generated template instance.
    :param template_dir: Absolute path to the template directory.
    :param context: Dict for populating the template's variables.
    """
    instance_subdir = instance_dir.absolute()
    if instance_subdir.exists():
        raise Exception(f"Instance (path) already exists: {template_dir} -> {instance_subdir}")
    
    env = create_env()
    with work_in(template_dir):
        env.loader = FileSystemLoader(["."])
        
        for root, dir_names, file_names in os.walk("."):
            for dir_name in dir_names:
                template_subdir_relative = Path(root, dir_name)
                render_directory(instance_dir, template_subdir_relative, context, env)
            
            for file_name in file_names:
                instance_file_relative = Path(root, file_name)
                render_file(instance_dir, instance_file_relative, context, env)


def use_template(
    instance: Path,
    template: Path,
    context: Context,
) -> None:
    """
    :param instance: Absolute path to the resulting generated template instance.
    :param template: Absolute path to the template.
    :param context: Dict for populating the template's variables.
    """
    template = template.absolute()
    if not template.exists():
        raise Exception(f"Template doesn't exist: {template}")
    
    if template.is_file():
        use_template_file(instance, template, context)
    
    if template.is_dir():
        use_template_dir(instance, template, context)
        