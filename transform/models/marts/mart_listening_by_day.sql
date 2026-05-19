with base as (
    select * from {{ ref('stg_played_tracks') }}
)

select
    played_date,
    count(*)                        as total_plays,
    count(distinct artist_name)     as unique_artists,
    round(sum(duration_minutes), 2) as total_minutes_listened
from base
group by played_date
order by played_date