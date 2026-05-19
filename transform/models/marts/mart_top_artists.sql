with base as (
    select * from {{ ref('stg_played_tracks') }}
)

select
    artist_name,
    count(*)                            as total_plays,
    count(distinct track_id)            as unique_tracks,
    round(sum(duration_minutes), 2)     as total_minutes_listened
from base
group by artist_name
order by total_plays desc