# -*- coding: utf-8 -*-

import enum
import textwrap

from ..chinook.chinook_data_model import (
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

class ChinookTableNameEnum(str, enum.Enum):
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


class ChinookViewNameEnum(str, enum.Enum):
    AlbumSalesStats = "AlbumSalesStats"


# Artist table - Small lookup table, use DISTSTYLE ALL for better joins
sql_create_table_artist = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS Artist (
    ArtistId INTEGER NOT NULL,
    Name VARCHAR(255),
    PRIMARY KEY (ArtistId)
)
DISTSTYLE ALL
SORTKEY (ArtistId);
"""
)

# Album table - Distribute by ArtistId for better joins with Artist
sql_create_table_album = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS Album (
    AlbumId INTEGER NOT NULL,
    Title VARCHAR(255) NOT NULL,
    ArtistId INTEGER NOT NULL,
    PRIMARY KEY (AlbumId),
    FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
)
DISTKEY (ArtistId)
SORTKEY (AlbumId, ArtistId);
"""
)

# Genre table - Small lookup table, use DISTSTYLE ALL
sql_create_table_genre = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS Genre (
    GenreId INTEGER NOT NULL,
    Name VARCHAR(255),
    PRIMARY KEY (GenreId)
)
DISTSTYLE ALL
SORTKEY (GenreId);
"""
)

# MediaType table - Small lookup table, use DISTSTYLE ALL
sql_create_table_mediatype = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS MediaType (
    MediaTypeId INTEGER NOT NULL,
    Name VARCHAR(255),
    PRIMARY KEY (MediaTypeId)
)
DISTSTYLE ALL
SORTKEY (MediaTypeId);
"""
)

# Track table - Main fact table, distribute by TrackId and sort by common query patterns
sql_create_table_track = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS Track (
    TrackId INTEGER NOT NULL,
    Name VARCHAR(500) NOT NULL,
    AlbumId INTEGER,
    MediaTypeId INTEGER NOT NULL,
    GenreId INTEGER,
    Composer VARCHAR(500),
    Milliseconds INTEGER NOT NULL,
    Bytes INTEGER,
    UnitPrice DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (TrackId),
    FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId),
    FOREIGN KEY (MediaTypeId) REFERENCES MediaType(MediaTypeId),
    FOREIGN KEY (GenreId) REFERENCES Genre(GenreId)
)
DISTKEY (TrackId)
SORTKEY (TrackId, AlbumId, GenreId);
"""
)

# Playlist table - Small table, use DISTSTYLE ALL
sql_create_table_playlist = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS Playlist (
    PlaylistId INTEGER NOT NULL,
    Name VARCHAR(255),
    PRIMARY KEY (PlaylistId)
)
DISTSTYLE ALL
SORTKEY (PlaylistId);
"""
)

# PlaylistTrack table - Junction table, distribute by TrackId for better joins with Track
sql_create_table_playlisttrack = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS PlaylistTrack (
    PlaylistId INTEGER NOT NULL,
    TrackId INTEGER NOT NULL,
    PRIMARY KEY (PlaylistId, TrackId),
    FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId),
    FOREIGN KEY (TrackId) REFERENCES Track(TrackId)
)
DISTKEY (TrackId)
SORTKEY (PlaylistId, TrackId);
"""
)

# Employee table - Small table, use DISTSTYLE ALL
sql_create_table_employee = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS Employee (
    EmployeeId INTEGER NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    FirstName VARCHAR(255) NOT NULL,
    Title VARCHAR(255),
    ReportsTo INTEGER,
    BirthDate TIMESTAMP,
    HireDate TIMESTAMP,
    Address VARCHAR(500),
    City VARCHAR(100),
    State VARCHAR(100),
    Country VARCHAR(100),
    PostalCode VARCHAR(20),
    Phone VARCHAR(50),
    Fax VARCHAR(50),
    Email VARCHAR(255),
    PRIMARY KEY (EmployeeId),
    FOREIGN KEY (ReportsTo) REFERENCES Employee(EmployeeId)
)
DISTSTYLE ALL
SORTKEY (EmployeeId);
"""
)

# Customer table - Distribute by CustomerId, sort by common query patterns
sql_create_table_customer = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS Customer (
    CustomerId INTEGER NOT NULL,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Company VARCHAR(255),
    Address VARCHAR(500),
    City VARCHAR(100),
    State VARCHAR(100),
    Country VARCHAR(100),
    PostalCode VARCHAR(20),
    Phone VARCHAR(50),
    Fax VARCHAR(50),
    Email VARCHAR(255) NOT NULL,
    SupportRepId INTEGER,
    PRIMARY KEY (CustomerId),
    FOREIGN KEY (SupportRepId) REFERENCES Employee(EmployeeId)
)
DISTKEY (CustomerId)
SORTKEY (CustomerId, Country, City);
"""
)

# Invoice table - Fact table, distribute by CustomerId for better joins
sql_create_table_invoice = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS Invoice (
    InvoiceId INTEGER NOT NULL,
    CustomerId INTEGER NOT NULL,
    InvoiceDate TIMESTAMP NOT NULL,
    BillingAddress VARCHAR(500),
    BillingCity VARCHAR(100),
    BillingState VARCHAR(100),
    BillingCountry VARCHAR(100),
    BillingPostalCode VARCHAR(20),
    Total DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (InvoiceId),
    FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
)
DISTKEY (CustomerId)
SORTKEY (InvoiceDate, CustomerId);
"""
)

# InvoiceLine table - Main fact table, distribute by InvoiceId for better joins with Invoice
sql_create_table_invoiceline = textwrap.dedent(
    """
CREATE TABLE IF NOT EXISTS InvoiceLine (
    InvoiceLineId INTEGER NOT NULL,
    InvoiceId INTEGER NOT NULL,
    TrackId INTEGER NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    Quantity INTEGER NOT NULL,
    PRIMARY KEY (InvoiceLineId),
    FOREIGN KEY (InvoiceId) REFERENCES Invoice(InvoiceId),
    FOREIGN KEY (TrackId) REFERENCES Track(TrackId)
)
DISTKEY (InvoiceId)
SORTKEY (InvoiceId, TrackId);
"""
)

# AlbumSalesStats view - Based on your SQLAlchemy select statement
sql_create_view_albumsalesstats = textwrap.dedent(
    """
CREATE OR REPLACE VIEW AlbumSalesStats AS
SELECT 
    a.AlbumId,
    a.Title AS AlbumTitle,
    ar.Name AS ArtistName,
    COUNT(DISTINCT il.InvoiceLineId)::INTEGER AS TotalSales,
    COALESCE(SUM(il.Quantity), 0)::INTEGER AS TotalQuantity,
    COALESCE(SUM(il.UnitPrice * il.Quantity), 0)::DECIMAL(10,2) AS TotalRevenue,
    COALESCE(ROUND(AVG(il.UnitPrice), 2), 0)::DECIMAL(10,2) AS AvgTrackPrice,
    COUNT(DISTINCT t.TrackId)::INTEGER AS TracksInAlbum
FROM Album a
JOIN Artist ar ON a.ArtistId = ar.ArtistId
JOIN Track t ON a.AlbumId = t.AlbumId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY a.AlbumId, a.Title, ar.Name
ORDER BY COALESCE(SUM(il.UnitPrice * il.Quantity), 0) DESC;
"""
)

# Complete DDL script that creates all tables in dependency order
sql_create_all_tables = textwrap.dedent(
    """
-- Create tables in dependency order to handle foreign key constraints

-- 1. Create lookup tables first (no dependencies)
{artist}

{genre}

{mediatype}

{employee}

-- 2. Create tables with single dependencies
{album}

{playlist}

{customer}

-- 3. Create tables with multiple dependencies
{track}

{playlisttrack}

{invoice}

-- 4. Create main fact table last
{invoiceline}

-- 5. Create views
{albumsalesstats_view}
"""
).format(
    artist=sql_create_table_artist.strip(),
    genre=sql_create_table_genre.strip(),
    mediatype=sql_create_table_mediatype.strip(),
    employee=sql_create_table_employee.strip(),
    album=sql_create_table_album.strip(),
    playlist=sql_create_table_playlist.strip(),
    customer=sql_create_table_customer.strip(),
    track=sql_create_table_track.strip(),
    playlisttrack=sql_create_table_playlisttrack.strip(),
    invoice=sql_create_table_invoice.strip(),
    invoiceline=sql_create_table_invoiceline.strip(),
    albumsalesstats_view=sql_create_view_albumsalesstats.strip(),
)

# Drop all tables and views script (in reverse dependency order)
sql_drop_all_tables = textwrap.dedent(
    """
-- Drop views first
DROP VIEW IF EXISTS AlbumSalesStats;

-- Drop tables in reverse dependency order (fact tables first, then dimension tables)
DROP TABLE IF EXISTS InvoiceLine;
DROP TABLE IF EXISTS Invoice;
DROP TABLE IF EXISTS PlaylistTrack;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS MediaType;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Artist;
"""
)

# Individual drop statements
sql_drop_view_albumsalesstats = "DROP VIEW IF EXISTS AlbumSalesStats;"
sql_drop_table_invoiceline = "DROP TABLE IF EXISTS InvoiceLine;"
sql_drop_table_invoice = "DROP TABLE IF EXISTS Invoice;"
sql_drop_table_playlisttrack = "DROP TABLE IF EXISTS PlaylistTrack;"
sql_drop_table_track = "DROP TABLE IF EXISTS Track;"
sql_drop_table_customer = "DROP TABLE IF EXISTS Customer;"
sql_drop_table_playlist = "DROP TABLE IF EXISTS Playlist;"
sql_drop_table_album = "DROP TABLE IF EXISTS Album;"
sql_drop_table_employee = "DROP TABLE IF EXISTS Employee;"
sql_drop_table_mediatype = "DROP TABLE IF EXISTS MediaType;"
sql_drop_table_genre = "DROP TABLE IF EXISTS Genre;"
sql_drop_table_artist = "DROP TABLE IF EXISTS Artist;"

# Dictionary for easy access to individual table scripts
table_creation_scripts = {
    "Artist": sql_create_table_artist,
    "Album": sql_create_table_album,
    "Genre": sql_create_table_genre,
    "MediaType": sql_create_table_mediatype,
    "Track": sql_create_table_track,
    "Playlist": sql_create_table_playlist,
    "PlaylistTrack": sql_create_table_playlisttrack,
    "Employee": sql_create_table_employee,
    "Customer": sql_create_table_customer,
    "Invoice": sql_create_table_invoice,
    "InvoiceLine": sql_create_table_invoiceline,
    "AlbumSalesStats": sql_create_view_albumsalesstats,
}

# Dictionary for easy access to individual drop scripts
table_drop_scripts = {
    "Artist": sql_drop_table_artist,
    "Album": sql_drop_table_album,
    "Genre": sql_drop_table_genre,
    "MediaType": sql_drop_table_mediatype,
    "Track": sql_drop_table_track,
    "Playlist": sql_drop_table_playlist,
    "PlaylistTrack": sql_drop_table_playlisttrack,
    "Employee": sql_drop_table_employee,
    "Customer": sql_drop_table_customer,
    "Invoice": sql_drop_table_invoice,
    "InvoiceLine": sql_drop_table_invoiceline,
    "AlbumSalesStats": sql_drop_view_albumsalesstats,
}
