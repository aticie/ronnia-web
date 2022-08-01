<script>
	import { createEventDispatcher } from "svelte";
	const dispatch = createEventDispatcher();

	export let min_value;
	export let max_value;
	export let key;

	function checkNaN(input) {
		return isNaN(parseFloat(input));
	}

	function checkMinusOne(input) {
		return parseFloat(input) === -1;
	}
	function checkPositive(input) {
		return parseFloat(input) > 0;
	}

	function validate_input() {
		if (!checkNaN(min_value) && !checkNaN(max_value)) {
			if (!(!checkPositive(min_value) && !checkMinusOne(min_value))) {
				if (!(!checkPositive(max_value) && !checkMinusOne(max_value))) {
					if (
						checkMinusOne(max_value) ||
						checkMinusOne(min_value) ||
						parseFloat(min_value) <= parseFloat(max_value)
					) {
						dispatch("message", {
							min_value,
							max_value,
						});
					} else {
						dispatch("message", {
							error:
								"Maximum " +
								key +
								" cannot be lower than minimum " +
								key,
						});
					}
				} else {
					dispatch("message", {
						error: "Incorrect max value",
					});
				}
			} else {
				dispatch("message", {
					error: "Incorrect min value",
				});
			}
		} else {
			dispatch("message", {
				error: "Incorrect value",
			});
		}
	}
</script>

<input
	type="text"
	name="min_input"
	bind:value={min_value}
	on:change={validate_input}
/>
<input
	type="text"
	name="max_input"
	bind:value={max_value}
	on:change={validate_input}
/>

<style>
	:global(input.invalid) {
		border-color: red;
	}
	input {
		margin: 4px 5px;
		width: 3rem;
		height: 1.5rem;
		font-size: 16pt;
		font-family: "Roboto", sans-serif;
		border: none;
		border-radius: 5%;
		color: white;
		background-color: rgb(60, 60, 60);
		text-align: center;
	}
	input[type="text"]:focus {
		border: none;
	}
</style>
