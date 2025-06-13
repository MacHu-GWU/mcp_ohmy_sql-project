# -*- coding: utf-8 -*-

import textwrap

import polars as pl

from ..chinook.chinook_data_model import (
    ChinookTableNameEnum,
    ChinookViewNameEnum,
    Artist,
    Album,
    Genre,
    MediaType,
    Track,
    Playlist,
    PlaylistTrack,
    Employee,
    Customer,
    Invoice,
    InvoiceLine,
)


# Artist table - Small lookup table, use DISTSTYLE ALL for better joins
sql_create_table_artist = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.Artist.value} (
    {Artist.ArtistId.name} INTEGER NOT NULL,
    {Artist.Name.name} VARCHAR(255),
    PRIMARY KEY ({Artist.ArtistId.name})
)
DISTSTYLE ALL
SORTKEY ({Artist.ArtistId.name});
"""
)

# Album table - Distribute by ArtistId for better joins with Artist
sql_create_table_album = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.Album.value} (
    {Album.AlbumId.name} INTEGER NOT NULL,
    {Album.Title.name} VARCHAR(255) NOT NULL,
    {Album.ArtistId.name} INTEGER NOT NULL,
    PRIMARY KEY ({Album.AlbumId.name}),
    FOREIGN KEY ({Album.ArtistId.name}) REFERENCES {ChinookTableNameEnum.Artist.value}({Artist.ArtistId.name})
)
DISTKEY ({Album.ArtistId.name})
SORTKEY ({Album.AlbumId.name}, {Album.ArtistId.name});
"""
)

# Genre table - Small lookup table, use DISTSTYLE ALL
sql_create_table_genre = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.Genre.value} (
    {Genre.GenreId.name} INTEGER NOT NULL,
    {Genre.Name.name} VARCHAR(255),
    PRIMARY KEY ({Genre.GenreId.name})
)
DISTSTYLE ALL
SORTKEY ({Genre.GenreId.name});
"""
)

# MediaType table - Small lookup table, use DISTSTYLE ALL
sql_create_table_mediatype = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.MediaType.value} (
    {MediaType.MediaTypeId.name} INTEGER NOT NULL,
    {MediaType.Name.name} VARCHAR(255),
    PRIMARY KEY ({MediaType.MediaTypeId.name})
)
DISTSTYLE ALL
SORTKEY ({MediaType.MediaTypeId.name});
"""
)

# Track table - Main fact table, distribute by TrackId and sort by common query patterns
sql_create_table_track = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.Track.value} (
    {Track.TrackId.name} INTEGER NOT NULL,
    {Track.Name.name} VARCHAR(500) NOT NULL,
    {Track.AlbumId.name} INTEGER,
    {Track.MediaTypeId.name} INTEGER NOT NULL,
    {Track.GenreId.name} INTEGER,
    {Track.Composer.name} VARCHAR(500),
    {Track.Milliseconds.name} INTEGER NOT NULL,
    {Track.Bytes.name} INTEGER,
    {Track.UnitPrice.name} DECIMAL(10,2) NOT NULL,
    PRIMARY KEY ({Track.TrackId.name}),
    FOREIGN KEY ({Track.AlbumId.name}) REFERENCES {ChinookTableNameEnum.Album.value}({Album.AlbumId.name}),
    FOREIGN KEY ({Track.MediaTypeId.name}) REFERENCES {ChinookTableNameEnum.MediaType.value}({MediaType.MediaTypeId.name}),
    FOREIGN KEY ({Track.GenreId.name}) REFERENCES {ChinookTableNameEnum.Genre.value}({Genre.GenreId.name})
)
DISTKEY ({Track.TrackId.name})
SORTKEY ({Track.TrackId.name}, {Track.AlbumId.name}, {Track.GenreId.name});
"""
)

# Playlist table - Small table, use DISTSTYLE ALL
sql_create_table_playlist = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.Playlist.value} (
    {Playlist.PlaylistId.name} INTEGER NOT NULL,
    {Playlist.Name.name} VARCHAR(255),
    PRIMARY KEY ({Playlist.PlaylistId.name})
)
DISTSTYLE ALL
SORTKEY ({Playlist.PlaylistId.name});
"""
)

# PlaylistTrack table - Junction table, distribute by TrackId for better joins with Track
sql_create_table_playlisttrack = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.PlaylistTrack.value} (
    {PlaylistTrack.PlaylistId.name} INTEGER NOT NULL,
    {PlaylistTrack.TrackId.name} INTEGER NOT NULL,
    PRIMARY KEY ({PlaylistTrack.PlaylistId.name}, {PlaylistTrack.TrackId.name}),
    FOREIGN KEY ({PlaylistTrack.PlaylistId.name}) REFERENCES {ChinookTableNameEnum.Playlist.value}({Playlist.PlaylistId.name}),
    FOREIGN KEY ({PlaylistTrack.TrackId.name}) REFERENCES {ChinookTableNameEnum.Track.value}({Track.TrackId.name})
)
DISTKEY ({PlaylistTrack.TrackId.name})
SORTKEY ({PlaylistTrack.PlaylistId.name}, {PlaylistTrack.TrackId.name});
"""
).strip()

# Employee table - Small table, use DISTSTYLE ALL
sql_create_table_employee = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.Employee.value} (
    {Employee.EmployeeId.name} INTEGER NOT NULL,
    {Employee.LastName.name} VARCHAR(255) NOT NULL,
    {Employee.FirstName.name} VARCHAR(255) NOT NULL,
    {Employee.Title.name} VARCHAR(255),
    {Employee.ReportsTo.name} INTEGER,
    {Employee.BirthDate.name} TIMESTAMP,
    {Employee.HireDate.name} TIMESTAMP,
    {Employee.Address.name} VARCHAR(500),
    {Employee.City.name} VARCHAR(100),
    {Employee.State.name} VARCHAR(100),
    {Employee.Country.name} VARCHAR(100),
    {Employee.PostalCode.name} VARCHAR(20),
    {Employee.Phone.name} VARCHAR(50),
    {Employee.Fax.name} VARCHAR(50),
    {Employee.Email.name} VARCHAR(255),
    PRIMARY KEY ({Employee.EmployeeId.name}),
    FOREIGN KEY ({Employee.ReportsTo.name}) REFERENCES {ChinookTableNameEnum.Employee.value}({Employee.EmployeeId.name})
)
DISTSTYLE ALL
SORTKEY ({Employee.EmployeeId.name});
"""
).strip()

# Customer table - Distribute by CustomerId, sort by common query patterns
sql_create_table_customer = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.Customer.value} (
    {Customer.CustomerId.name} INTEGER NOT NULL,
    {Customer.FirstName.name} VARCHAR(255) NOT NULL,
    {Customer.LastName.name} VARCHAR(255) NOT NULL,
    {Customer.Company.name} VARCHAR(255),
    {Customer.Address.name} VARCHAR(500),
    {Customer.City.name} VARCHAR(100),
    {Customer.State.name} VARCHAR(100),
    {Customer.Country.name} VARCHAR(100),
    {Customer.PostalCode.name} VARCHAR(20),
    {Customer.Phone.name} VARCHAR(50),
    {Customer.Fax.name} VARCHAR(50),
    {Customer.Email.name} VARCHAR(255) NOT NULL,
    {Customer.SupportRepId.name} INTEGER,
    PRIMARY KEY ({Customer.CustomerId.name}),
    FOREIGN KEY ({Customer.SupportRepId.name}) REFERENCES {ChinookTableNameEnum.Employee.value}({Employee.EmployeeId.name})
)
DISTKEY ({Customer.CustomerId.name})
SORTKEY ({Customer.CustomerId.name}, {Customer.Country.name}, {Customer.City.name});
"""
).strip()

# Invoice table - Fact table, distribute by CustomerId for better joins
sql_create_table_invoice = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.Invoice.value} (
    {Invoice.InvoiceId.name} INTEGER NOT NULL,
    {Invoice.CustomerId.name} INTEGER NOT NULL,
    {Invoice.InvoiceDate.name} TIMESTAMP NOT NULL,
    {Invoice.BillingAddress.name} VARCHAR(500),
    {Invoice.BillingCity.name} VARCHAR(100),
    {Invoice.BillingState.name} VARCHAR(100),
    {Invoice.BillingCountry.name} VARCHAR(100),
    {Invoice.BillingPostalCode.name} VARCHAR(20),
    {Invoice.Total.name} DECIMAL(10,2) NOT NULL,
    PRIMARY KEY ({Invoice.InvoiceId.name}),
    FOREIGN KEY ({Invoice.CustomerId.name}) REFERENCES {ChinookTableNameEnum.Customer.value}({Customer.CustomerId.name})
)
DISTKEY ({Invoice.CustomerId.name})
SORTKEY ({Invoice.InvoiceDate.name}, {Invoice.CustomerId.name});
"""
).strip()

# InvoiceLine table - Main fact table, distribute by InvoiceId for better joins with Invoice
sql_create_table_invoiceline = textwrap.dedent(
    f"""
CREATE TABLE IF NOT EXISTS {ChinookTableNameEnum.InvoiceLine.value} (
    {InvoiceLine.InvoiceLineId.name} INTEGER NOT NULL,
    {InvoiceLine.InvoiceId.name} INTEGER NOT NULL,
    {InvoiceLine.TrackId.name} INTEGER NOT NULL,
    {InvoiceLine.UnitPrice.name} DECIMAL(10,2) NOT NULL,
    {InvoiceLine.Quantity.name} INTEGER NOT NULL,
    PRIMARY KEY ({InvoiceLine.InvoiceLineId.name}),
    FOREIGN KEY ({InvoiceLine.InvoiceId.name}) REFERENCES {ChinookTableNameEnum.Invoice.value}({Invoice.InvoiceId.name}),
    FOREIGN KEY ({InvoiceLine.TrackId.name}) REFERENCES {ChinookTableNameEnum.Track.value}({Track.TrackId.name})
)
DISTKEY ({InvoiceLine.InvoiceId.name})
SORTKEY ({InvoiceLine.InvoiceId.name}, {InvoiceLine.TrackId.name});
"""
).strip()

# AlbumSalesStats view - Based on your SQLAlchemy select statement
sql_create_view_albumsalesstats = textwrap.dedent(
    f"""
CREATE OR REPLACE VIEW {ChinookViewNameEnum.AlbumSalesStats.value} AS
SELECT 
    a.{Album.AlbumId.name},
    a.{Album.Title.name} AS AlbumTitle,
    ar.{Artist.Name.name} AS ArtistName,
    COUNT(DISTINCT il.{InvoiceLine.InvoiceLineId.name})::INTEGER AS TotalSales,
    COALESCE(SUM(il.{InvoiceLine.Quantity.name}), 0)::INTEGER AS TotalQuantity,
    COALESCE(SUM(il.{InvoiceLine.UnitPrice.name} * il.{InvoiceLine.Quantity.name}), 0)::DECIMAL(10,2) AS TotalRevenue,
    COALESCE(ROUND(AVG(il.{InvoiceLine.UnitPrice.name}), 2), 0)::DECIMAL(10,2) AS AvgTrackPrice,
    COUNT(DISTINCT t.{Track.TrackId.name})::INTEGER AS TracksInAlbum
FROM {ChinookTableNameEnum.Album.value} a
JOIN {ChinookTableNameEnum.Artist.value} ar ON a.{Album.ArtistId.name} = ar.{Artist.ArtistId.name}
JOIN {ChinookTableNameEnum.Track.value} t ON a.{Album.AlbumId.name} = t.{Track.AlbumId.name}
LEFT JOIN {ChinookTableNameEnum.InvoiceLine.value} il ON t.{Track.TrackId.name} = il.{InvoiceLine.TrackId.name}
GROUP BY a.{Album.AlbumId.name}, a.{Album.Title.name}, ar.{Artist.Name.name}
ORDER BY COALESCE(SUM(il.{InvoiceLine.UnitPrice.name} * il.{InvoiceLine.Quantity.name}), 0) DESC;
"""
).strip()

# Complete DDL script that creates all tables in dependency order
sql_create_all_tables = textwrap.dedent(
    f"""
-- Create tables in dependency order to handle foreign key constraints

-- 1. Create lookup tables first (no dependencies)
{sql_create_table_artist}

{sql_create_table_genre}

{sql_create_table_mediatype}

{sql_create_table_employee}

-- 2. Create tables with single dependencies
{sql_create_table_album}

{sql_create_table_playlist}

{sql_create_table_customer}

-- 3. Create tables with multiple dependencies
{sql_create_table_track}

{sql_create_table_playlisttrack}

{sql_create_table_invoice}

-- 4. Create main fact table last
{sql_create_table_invoiceline}

-- 5. Create views
{sql_create_view_albumsalesstats}
"""
).strip()

# Individual drop statements using enum values
# fmt: off
sql_drop_view_albumsalesstats = f"DROP VIEW IF EXISTS {ChinookViewNameEnum.AlbumSalesStats.value};"
sql_drop_table_invoiceline = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.InvoiceLine.value};"
sql_drop_table_invoice = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.Invoice.value};"
sql_drop_table_playlisttrack = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.PlaylistTrack.value};"
sql_drop_table_track = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.Track.value};"
sql_drop_table_customer = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.Customer.value};"
sql_drop_table_playlist = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.Playlist.value};"
sql_drop_table_album = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.Album.value};"
sql_drop_table_employee = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.Employee.value};"
sql_drop_table_mediatype = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.MediaType.value};"
sql_drop_table_genre = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.Genre.value};"
sql_drop_table_artist = f"DROP TABLE IF EXISTS {ChinookTableNameEnum.Artist.value};"
# fmt: on

# Drop all tables and views script using f-string composition
sql_drop_all_tables = f"""
-- Drop views first
{sql_drop_view_albumsalesstats}

-- Drop tables in reverse dependency order (fact tables first, then dimension tables)
{sql_drop_table_invoiceline}
{sql_drop_table_invoice}
{sql_drop_table_playlisttrack}
{sql_drop_table_track}
{sql_drop_table_customer}
{sql_drop_table_playlist}
{sql_drop_table_album}
{sql_drop_table_employee}
{sql_drop_table_mediatype}
{sql_drop_table_genre}
{sql_drop_table_artist}
"""

# Dictionary for easy access to individual table scripts
table_creation_scripts = {
    ChinookTableNameEnum.Artist.value: sql_create_table_artist,
    ChinookTableNameEnum.Album.value: sql_create_table_album,
    ChinookTableNameEnum.Genre.value: sql_create_table_genre,
    ChinookTableNameEnum.MediaType.value: sql_create_table_mediatype,
    ChinookTableNameEnum.Track.value: sql_create_table_track,
    ChinookTableNameEnum.Playlist.value: sql_create_table_playlist,
    ChinookTableNameEnum.PlaylistTrack.value: sql_create_table_playlisttrack,
    ChinookTableNameEnum.Employee.value: sql_create_table_employee,
    ChinookTableNameEnum.Customer.value: sql_create_table_customer,
    ChinookTableNameEnum.Invoice.value: sql_create_table_invoice,
    ChinookTableNameEnum.InvoiceLine.value: sql_create_table_invoiceline,
    ChinookViewNameEnum.AlbumSalesStats.value: sql_create_view_albumsalesstats,
}

# Dictionary for easy access to individual drop scripts (reordered: views first, then reverse dependency order)
table_drop_scripts = {
    # Views first
    ChinookViewNameEnum.AlbumSalesStats.value: sql_drop_view_albumsalesstats,
    # Fact tables (most dependent)
    ChinookTableNameEnum.InvoiceLine.value: sql_drop_table_invoiceline,
    ChinookTableNameEnum.Invoice.value: sql_drop_table_invoice,
    ChinookTableNameEnum.PlaylistTrack.value: sql_drop_table_playlisttrack,
    ChinookTableNameEnum.Track.value: sql_drop_table_track,
    # Dimension tables with dependencies
    ChinookTableNameEnum.Customer.value: sql_drop_table_customer,
    ChinookTableNameEnum.Album.value: sql_drop_table_album,
    # Lookup tables (least dependent)
    ChinookTableNameEnum.Playlist.value: sql_drop_table_playlist,
    ChinookTableNameEnum.Employee.value: sql_drop_table_employee,
    ChinookTableNameEnum.MediaType.value: sql_drop_table_mediatype,
    ChinookTableNameEnum.Genre.value: sql_drop_table_genre,
    ChinookTableNameEnum.Artist.value: sql_drop_table_artist,
}


# Artist table schema
pl_schema_artist = {"ArtistId": pl.Int32, "Name": pl.Utf8}

# Album table schema
pl_schema_album = {"AlbumId": pl.Int32, "Title": pl.Utf8, "ArtistId": pl.Int32}

# Genre table schema
pl_schema_genre = {"GenreId": pl.Int32, "Name": pl.Utf8}

# MediaType table schema
pl_schema_mediatype = {"MediaTypeId": pl.Int32, "Name": pl.Utf8}

# Track table schema
pl_schema_track = {
    "TrackId": pl.Int32,
    "Name": pl.Utf8,
    "AlbumId": pl.Int32,
    "MediaTypeId": pl.Int32,
    "GenreId": pl.Int32,
    "Composer": pl.Utf8,
    "Milliseconds": pl.Int32,
    "Bytes": pl.Int32,
    "UnitPrice": pl.Decimal(precision=10, scale=2),
}

# Playlist table schema
pl_schema_playlist = {"PlaylistId": pl.Int32, "Name": pl.Utf8}

# PlaylistTrack table schema
pl_schema_playlisttrack = {"PlaylistId": pl.Int32, "TrackId": pl.Int32}

# Employee table schema
pl_schema_employee = {
    "EmployeeId": pl.Int32,
    "LastName": pl.Utf8,
    "FirstName": pl.Utf8,
    "Title": pl.Utf8,
    "ReportsTo": pl.Int32,
    "BirthDate": pl.Datetime,
    "HireDate": pl.Datetime,
    "Address": pl.Utf8,
    "City": pl.Utf8,
    "State": pl.Utf8,
    "Country": pl.Utf8,
    "PostalCode": pl.Utf8,
    "Phone": pl.Utf8,
    "Fax": pl.Utf8,
    "Email": pl.Utf8,
}

# Customer table schema
pl_schema_customer = {
    "CustomerId": pl.Int32,
    "FirstName": pl.Utf8,
    "LastName": pl.Utf8,
    "Company": pl.Utf8,
    "Address": pl.Utf8,
    "City": pl.Utf8,
    "State": pl.Utf8,
    "Country": pl.Utf8,
    "PostalCode": pl.Utf8,
    "Phone": pl.Utf8,
    "Fax": pl.Utf8,
    "Email": pl.Utf8,
    "SupportRepId": pl.Int32,
}

# Invoice table schema
pl_schema_invoice = {
    "InvoiceId": pl.Int32,
    "CustomerId": pl.Int32,
    "InvoiceDate": pl.Datetime,
    "BillingAddress": pl.Utf8,
    "BillingCity": pl.Utf8,
    "BillingState": pl.Utf8,
    "BillingCountry": pl.Utf8,
    "BillingPostalCode": pl.Utf8,
    "Total": pl.Decimal(precision=10, scale=2),
}

# InvoiceLine table schema
pl_schema_invoiceline = {
    "InvoiceLineId": pl.Int32,
    "InvoiceId": pl.Int32,
    "TrackId": pl.Int32,
    "UnitPrice": pl.Decimal(precision=10, scale=2),
    "Quantity": pl.Int32,
}

polars_schemas = {
    ChinookTableNameEnum.Artist.value: pl_schema_artist,
    ChinookTableNameEnum.Album.value: pl_schema_album,
    ChinookTableNameEnum.Genre.value: pl_schema_genre,
    ChinookTableNameEnum.MediaType.value: pl_schema_mediatype,
    ChinookTableNameEnum.Track.value: pl_schema_track,
    ChinookTableNameEnum.Playlist.value: pl_schema_playlist,
    ChinookTableNameEnum.PlaylistTrack.value: pl_schema_playlisttrack,
    ChinookTableNameEnum.Employee.value: pl_schema_employee,
    ChinookTableNameEnum.Customer.value: pl_schema_customer,
    ChinookTableNameEnum.Invoice.value: pl_schema_invoice,
    ChinookTableNameEnum.InvoiceLine.value: pl_schema_invoiceline,
    ChinookViewNameEnum.AlbumSalesStats.value: sql_create_view_albumsalesstats,
}
