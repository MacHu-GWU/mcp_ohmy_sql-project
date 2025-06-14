# -*- coding: utf-8 -*-

"""
chinook database ORM Model definition.
"""

import typing as T
from decimal import Decimal
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from enum_mate.api import BetterStrEnum


class Base(orm.DeclarativeBase):
    """
    Ref: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
    """


class ChinookTableNameEnum(BetterStrEnum):
    """
    Note: The order of the enum members should match the order of table creation.
    """

    Artist = "Artist"
    Album = "Album"
    Genre = "Genre"
    MediaType = "MediaType"
    Track = "Track"
    Playlist = "Playlist"
    PlaylistTrack = "PlaylistTrack"
    Employee = "Employee"
    Customer = "Customer"
    Invoice = "Invoice"
    InvoiceLine = "InvoiceLine"


class ChinookViewNameEnum(BetterStrEnum):
    """
    Note: The order of the enum members should match the order of view creation.
    """

    AlbumSalesStats = "AlbumSalesStats"


# Note: The order of the enum members should match the order of table creation
# fmt: off
class Artist(Base):
    __tablename__ = ChinookTableNameEnum.Artist.value

    ArtistId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


class Album(Base):
    __tablename__ = ChinookTableNameEnum.Album.value

    AlbumId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Title: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    ArtistId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Artist.value}.{Artist.ArtistId.name}"), nullable=False)


class Genre(Base):
    __tablename__ = ChinookTableNameEnum.Genre.value

    GenreId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


class MediaType(Base):
    __tablename__ = ChinookTableNameEnum.MediaType.value

    MediaTypeId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


class Track(Base):
    __tablename__ = ChinookTableNameEnum.Track.value

    TrackId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    AlbumId: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Album.value}.{Album.AlbumId.name}"), nullable=True)
    MediaTypeId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.MediaType.value}.{MediaType.MediaTypeId.name}"), nullable=False)
    GenreId: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Genre.value}.{Genre.GenreId.name}"), nullable=True)
    Composer: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Milliseconds: orm.Mapped[int] = sa.Column(sa.Integer, nullable=False)
    Bytes: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, nullable=True)
    UnitPrice: orm.Mapped[Decimal] = sa.Column(sa.DECIMAL(10, 2), nullable=False)


class Playlist(Base):
    __tablename__ = ChinookTableNameEnum.Playlist.value

    PlaylistId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


class PlaylistTrack(Base):
    __tablename__ = ChinookTableNameEnum.PlaylistTrack.value

    PlaylistId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Playlist.value}.{Playlist.PlaylistId.name}"), primary_key=True)
    TrackId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Track.value}.{Track.TrackId.name}"), primary_key=True)


class Employee(Base):
    __tablename__ = ChinookTableNameEnum.Employee.value

    EmployeeId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    LastName: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    FirstName: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    Title: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    ReportsTo: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Employee.value}.EmployeeId"), nullable=True)
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
    __tablename__ = ChinookTableNameEnum.Customer.value

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
    SupportRepId: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Employee.value}.{Employee.EmployeeId.name}"), nullable=True)


class Invoice(Base):
    __tablename__ = ChinookTableNameEnum.Invoice.value

    InvoiceId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    CustomerId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Customer.value}.{Customer.CustomerId.name}"), nullable=False)
    InvoiceDate: orm.Mapped[datetime] = sa.Column(sa.DateTime, nullable=False)
    BillingAddress: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    BillingCity: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    BillingState: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    BillingCountry: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    BillingPostalCode: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    Total: orm.Mapped[Decimal] = sa.Column(sa.DECIMAL(10, 2), nullable=False)


class InvoiceLine(Base):
    __tablename__ = ChinookTableNameEnum.InvoiceLine.value

    InvoiceLineId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    InvoiceId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Invoice.value}.{Invoice.InvoiceId.name}"), nullable=False)
    TrackId: orm.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey(f"{ChinookTableNameEnum.Track.value}.{Track.TrackId.name}"), nullable=False)
    UnitPrice: orm.Mapped[Decimal] = sa.Column(sa.DECIMAL(10, 2), nullable=False)
    Quantity: orm.Mapped[int] = sa.Column(sa.Integer, nullable=False)
# fmt: on


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

VIEW_NAME_AND_SELECT_STMT_MAP: T.Dict[str, sa.Select] = {
    ChinookViewNameEnum.AlbumSalesStats.value: album_sales_stats_view_select_stmt,
}
