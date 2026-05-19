with source as (
    select * from {{ source('spotify', 'played_tracks') }}
),

renamed as (
    select
        played_at,
        track_id,
        track_name,
        artist_name,
        album_name,
        duration_ms,
        round(duration_ms / 60000.0, 2)      as duration_minutes,
        date(played_at)                       as played_date,
        extract(hour from played_at)          as played_hour,
        to_char(extract(hour from played_at), '00') || ':00' as hour_label,
        extract(dow from played_at)           as day_of_week
    from source
)

select * from renamed