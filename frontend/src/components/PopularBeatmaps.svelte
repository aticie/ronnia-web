<script>
    import axios from "axios";

    let beatmaps = []

    axios
        .get("/beatmaps/most_requested")
        .then((res) => {
                beatmaps = res.data
            }
        )


</script>


<div>
    <table>
        {#each beatmaps as bmap}
            <div class="beatmap_id">
                {axios.get('https://osu.ppy.sh/api/get_beatmaps', {
                    params: {
                        k: import.meta.env.VITE_OSU_API_KEY,
                        b: bmap.beatmap_id
                    }
                }).then(
                    (res) => {res}
                )}
            </div>
        {/each}
    </table>
</div>