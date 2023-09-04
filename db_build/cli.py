import click
import pathlib
import sqlite_utils
from sqlite_utils.utils import TypeTracker, rows_from_file

def define_db_name():
    "Define database name when no parameter is passed"
    path = pathlib.Path().resolve()
    default_db = path.name + '.db'
    dbs = [db.name for db in path.iterdir() if pathlib.Path(db).suffix in ('.db',)]
    if len(dbs) == 1:
        return dbs[0]
    return default_db

def get_files_paths(paths):
    "Get files and files in folders"
    extended = []
    for path in paths:
        p = pathlib.Path(path)
        if p.is_dir():
            extended.extend(list(p.iterdir()))
        else:
            extended.append(p)
    return extended

@click.command()
@click.argument(
    "database",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=False,
)
@click.argument(
    "paths",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, allow_dash=True),
    nargs=-1,
)
def cli(database, paths):
    "Build a SQLite database from files and directories"

    if database is None:
        database = define_db_name()
    db = sqlite_utils.Database(database)

    if len(paths)==0:
        paths=('.')

    paths = get_files_paths(paths)
    
    for path in paths:
        if path.suffix == ".csv":
            with path.open("rb") as fp:
                rows, _ = rows_from_file(fp)
                tracker = TypeTracker()
                db[path.stem].insert_all(tracker.wrap(rows))
    
