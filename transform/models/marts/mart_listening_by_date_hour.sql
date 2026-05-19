with base as (
    select * from {{ ref('stg_played_tracks') }}
)

select
    played_date,
    played_hour,
    to_char(played_hour, '00') || ':00'  as hour_label,
    count(*)                             as total_plays,
    round(sum(duration_minutes), 2)      as total_minutes_listened
from base
group by played_date, played_hour
order by played_date, played_hour