from click.testing import CliRunner
from db_build.cli import cli
import pathlib
import sqlite_utils
import shutil

examples = pathlib.Path(__file__).parent / "examples"


def test_basic_csv(tmpdir):
    runner = CliRunner()
    db_path = str(tmpdir / "data.db")
    result = runner.invoke(cli, [str(db_path), str(examples / "test.csv")])
    db = sqlite_utils.Database(db_path)
    assert db.schema == (
        "CREATE TABLE [test] (\n"
        "   [county] TEXT,\n"
        "   [precinct] TEXT,\n"
        "   [office] TEXT,\n"
        "   [district] TEXT,\n"
        "   [party] TEXT,\n"
        "   [candidate] TEXT,\n"
        "   [votes] TEXT\n"
        ");"
    )

def test_basic_folder(tmpdir):
    runner = CliRunner()
    db_path = str(tmpdir / "data.db")
    result = runner.invoke(cli, [str(db_path), str(examples)])
    db = sqlite_utils.Database(db_path)
    assert db.schema == (
        "CREATE TABLE [test] (\n"
        "   [county] TEXT,\n"
        "   [precinct] TEXT,\n"
        "   [office] TEXT,\n"
        "   [district] TEXT,\n"
        "   [party] TEXT,\n"
        "   [candidate] TEXT,\n"
        "   [votes] TEXT\n"
        ");"
    )

def test_no_args(tmpdir):
    runner = CliRunner()
    with runner.isolated_filesystem(tmpdir) as td:
        dst = pathlib.Path(td)
        db_path = str(dst / (dst.name + '.db'))
        shutil.copy(str(examples / 'test.csv'), str(dst / 'test.csv'))
        result = runner.invoke(cli)
    db = sqlite_utils.Database(db_path)
    assert db.schema == (
        "CREATE TABLE [test] (\n"
        "   [county] TEXT,\n"
        "   [precinct] TEXT,\n"
        "   [office] TEXT,\n"
        "   [district] TEXT,\n"
        "   [party] TEXT,\n"
        "   [candidate] TEXT,\n"
        "   [votes] TEXT\n"
        ");"
    )