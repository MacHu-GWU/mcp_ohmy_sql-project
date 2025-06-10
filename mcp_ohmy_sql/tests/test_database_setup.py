# -*- coding: utf-8 -*-

"""
Test Database Setup Module

This module provides automated setup functionality for creating and populating test databases
with the Chinook sample dataset. It supports multiple database backends including SQLite and
PostgreSQL, making it easy to provision identical test environments across different database
systems.

Key Features:

- Automated schema creation using SQLAlchemy ORM models
- Data population from Chinook JSON dataset
- Cross-database compatibility (SQLite, PostgreSQL)
- Sample view creation for testing complex queries
- Idempotent operations (safe to run multiple times)

Typical Usage:
    >>> from mcp_ohmy_sql.tests.test_database_setup import setup_test_database, EngineEnum
    >>> 
    >>> # Setup SQLite test database
    >>> setup_test_database(EngineEnum.sqlite)
    >>> 
    >>> # Setup PostgreSQL test database
    >>> setup_test_database(EngineEnum.postgres)
"""

import typing as T
import enum
import json
from decimal import Decimal
from datetime import datetime
from functools import cached_property

import sqlalchemy as sa
import sqlalchemy.orm as orm

from .chinook import path_ChinookData_json
from .test_config import DatabaseEnum


class Base(orm.DeclarativeBase):
    """
    Ref: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
    """


# fmt: off
class Artist(Base):
    __tablename__ = "Artist"

    ArtistId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


class Album(Base):
    __tablename__ = "Album"

    AlbumId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Title: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    ArtistId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("Artist.ArtistId"), nullable=False)


class Genre(Base):
    __tablename__ = "Genre"

    GenreId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


class MediaType(Base):
    __tablename__ = "MediaType"

    MediaTypeId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


class Track(Base):
    __tablename__ = "Track"

    TrackId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    AlbumId: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey("Album.AlbumId"), nullable=True)
    MediaTypeId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("MediaType.MediaTypeId"), nullable=False)
    GenreId: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey("Genre.GenreId"), nullable=True)
    Composer: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Milliseconds: orm.Mapped[int] = sa.Column(sa.Integer, nullable=False)
    Bytes: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, nullable=True)
    UnitPrice: orm.Mapped[Decimal] = sa.Column(sa.DECIMAL(10, 2), nullable=False)


class Playlist(Base):
    __tablename__ = "Playlist"

    PlaylistId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


class PlaylistTrack(Base):
    __tablename__ = "PlaylistTrack"

    PlaylistId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("Playlist.PlaylistId"), primary_key=True)
    TrackId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("Track.TrackId"), primary_key=True)


class Employee(Base):
    __tablename__ = "Employee"

    EmployeeId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    LastName: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    FirstName: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    Title: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    ReportsTo: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey("Employee.EmployeeId"), nullable=True)
    BirthDate: orm.Mapped[T.Optional[datetime]] = sa.Column(sa.DateTime, nullable=True)
    HireDate: orm.Mapped[T.Optional[datetime]] = sa.Column(sa.DateTime, nullable=True)
    Address: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    City: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    State: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Country: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    PostalCode: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Phone: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Fax: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Email: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)

    
class Customer(Base):
    __tablename__ = "Customer"

    CustomerId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    FirstName: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    LastName: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    Company: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Address: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    City: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    State: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Country: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    PostalCode: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Phone: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Fax: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Email: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    SupportRepId: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey("Employee.EmployeeId"), nullable=True)


class Invoice(Base):
    __tablename__ = "Invoice"

    InvoiceId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    CustomerId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("Customer.CustomerId"), nullable=False)
    InvoiceDate: orm.Mapped[datetime] = sa.Column(sa.DateTime, nullable=False)
    BillingAddress: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    BillingCity: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    BillingState: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    BillingCountry: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    BillingPostalCode: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Total: orm.Mapped[Decimal] = sa.Column(sa.DECIMAL(10, 2), nullable=False)


class InvoiceLine(Base):
    __tablename__ = "InvoiceLine"

    InvoiceLineId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    InvoiceId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("Invoice.InvoiceId"), nullable=False)
    TrackId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("Track.TrackId"), nullable=False)
    UnitPrice: orm.Mapped[Decimal] = sa.Column(sa.DECIMAL(10, 2), nullable=False)
    Quantity: orm.Mapped[int] = sa.Column(sa.Integer, nullable=False)
# fmt: on


class ViewNameEnum(str, enum.Enum):
    AlbumSalesStats = "AlbumSalesStats"


album_sales_stats_view_select_stmt = (
    sa.select(
        Album.AlbumId,
        Album.Title.label("AlbumTitle"),
        Artist.Name.label("ArtistName"),
        sa.cast(
            sa.func.count(sa.func.distinct(InvoiceLine.InvoiceLineId)), sa.Integer
        ).label("TotalSales"),
        sa.cast(
            sa.func.coalesce(sa.func.sum(InvoiceLine.Quantity), 0), sa.Integer
        ).label("TotalQuantity"),
        sa.cast(
            sa.func.coalesce(
                sa.func.sum(InvoiceLine.UnitPrice * InvoiceLine.Quantity), 0
            ),
            sa.DECIMAL(10, 2),
        ).label("TotalRevenue"),
        sa.cast(
            sa.func.coalesce(sa.func.round(sa.func.avg(InvoiceLine.UnitPrice), 2), 0),
            sa.DECIMAL(10, 2),
        ).label("AvgTrackPrice"),
        sa.cast(sa.func.count(sa.func.distinct(Track.TrackId)), sa.Integer).label(
            "TracksInAlbum"
        ),
    )
    .select_from(
        Album.__table__.join(Artist.__table__, Album.ArtistId == Artist.ArtistId)
        .join(Track.__table__, Album.AlbumId == Track.AlbumId)
        .outerjoin(InvoiceLine.__table__, Track.TrackId == InvoiceLine.TrackId)
    )
    .group_by(Album.AlbumId, Album.Title, Artist.Name)
    .order_by(
        sa.func.coalesce(
            sa.func.sum(InvoiceLine.UnitPrice * InvoiceLine.Quantity), 0
        ).desc()
    )
)


class _EngineEnum:
    @cached_property
    def sqlite(self) -> sa.engine.Engine:
        kwargs = DatabaseEnum.chinook_sqlite.connection.create_engine_kwargs
        return sa.create_engine(**kwargs)

    @cached_property
    def postgres(self) -> sa.engine.Engine:
        kwargs = DatabaseEnum.chinook_postgres.connection.create_engine_kwargs
        return sa.create_engine(**kwargs)


EngineEnum = _EngineEnum()


def drop_view(engine: sa.engine.Engine, view_name: str):
    with engine.connect() as conn:
        drop_view_sql = f'DROP VIEW IF EXISTS "{view_name}"'
        conn.execute(sa.text(drop_view_sql))
        conn.commit()


def drop_all_views(engine: sa.engine.Engine):
    for view_name in ViewNameEnum:
        drop_view(engine, view_name.value)


def setup_test_database(engine: sa.engine.Engine) -> None:
    """
    Set up a complete test database with Chinook sample data and views.

    This function performs a comprehensive database setup by:

    1. Dropping all existing tables (if any) to ensure a clean state
    2. Creating all tables using SQLAlchemy ORM models based on the Chinook schema
    3. Loading sample data from the Chinook JSON dataset
    4. Converting datetime strings to proper datetime objects for database compatibility
    5. Creating sample views (like AlbumSalesStats) for testing complex queries

    The setup is idempotent - it can be run multiple times safely as it drops
    existing tables before recreation.

    Example:

        >>> from mcp_ohmy_sql.tests.test_database_setup import setup_test_database, EngineEnum
        >>>
        >>> # Setup SQLite test database
        >>> setup_test_database(EngineEnum.sqlite)
        >>>
        >>> # Setup PostgreSQL test database (requires running postgres container)
        >>> setup_test_database(EngineEnum.postgres)

    .. note::

        - For PostgreSQL, ensure the database server is running and accessible
        - The function automatically handles database-specific SQL differences
        - All foreign key relationships are properly maintained during data insertion
    """
    drop_all_views(engine)

    with engine.connect() as conn:
        Base.metadata.drop_all(engine, checkfirst=True)
        Base.metadata.create_all(engine, checkfirst=True)
        conn.commit()

    data = json.loads(path_ChinookData_json.read_text())
    with engine.connect() as conn:
        for table in Base.metadata.sorted_tables:
            stmt = sa.insert(table)
            rows = data[table.name]
            for col_name, col in table.columns.items():
                if isinstance(col.type, sa.DateTime):
                    for row in rows:
                        try:
                            row[col_name] = datetime.fromisoformat(row[col_name])
                        except ValueError:
                            pass
            conn.execute(stmt, rows)
        conn.commit()

    # Get table references
    with engine.connect() as conn:
        select_sql = album_sales_stats_view_select_stmt.compile(
            engine,
            compile_kwargs={"literal_binds": True},
        )
        create_view_sql = f'CREATE VIEW "AlbumSalesStats" AS {select_sql}'
        # print(create_view_sql)
        conn.execute(sa.text(create_view_sql))
        conn.commit()
