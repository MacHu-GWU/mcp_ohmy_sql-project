# -*- coding: utf-8 -*-

import typing as T
import json
from decimal import Decimal
from datetime import datetime
from functools import cached_property

import sqlalchemy as sa
import sqlalchemy.orm as orm
from .chinook import dir_tmp, path_ChinookData_json


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

album_sales_stats_view_select_stmt = (
    sa.select(
        Album.AlbumId,
        Album.Title.label("AlbumTitle"),
        Artist.Name.label("ArtistName"),
        sa.func.count(sa.func.distinct(InvoiceLine.InvoiceLineId)).label("TotalSales"),
        sa.func.sum(InvoiceLine.Quantity).label("TotalQuantity"),
        sa.func.sum(InvoiceLine.UnitPrice * InvoiceLine.Quantity).label("TotalRevenue"),
        sa.func.round(sa.func.avg(InvoiceLine.UnitPrice), 2).label("AvgTrackPrice"),
        sa.func.count(sa.func.distinct(Track.TrackId)).label("TracksInAlbum"),
    )
    .select_from(
        Album.__table__.join(Artist.__table__, Album.ArtistId == Artist.ArtistId)
        .join(Track.__table__, Album.AlbumId == Track.AlbumId)
        .join(InvoiceLine.__table__, Track.TrackId == InvoiceLine.TrackId)
    )
    .group_by(Album.AlbumId, Album.Title, Artist.Name)
    .order_by(sa.func.sum(InvoiceLine.UnitPrice * InvoiceLine.Quantity).desc())
)


class _EngineEnum:
    @cached_property
    def sqlite(self) -> sa.engine.Engine:
        path = dir_tmp / "Chinook_Sqlite.sqlite"
        path.unlink(missing_ok=True)
        return sa.create_engine(f"sqlite:///{path}")

    @cached_property
    def postgres(self) -> sa.engine.Engine:
        return sa.create_engine(
            "postgresql+psycopg2://postgres:password@localhost:40311/postgres"
        )


EngineEnum = _EngineEnum()


def prepare_data(engine: sa.engine.Engine):
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
        create_view_sql = f"CREATE VIEW \"AlbumSalesStats\" AS {select_sql}"
        print(create_view_sql)
        conn.execute(sa.text(create_view_sql))
        conn.commit()
