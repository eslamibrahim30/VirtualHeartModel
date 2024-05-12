import numpy as np

def gauss_weight(distance: float, theta: float) -> float:
  """
  Calculates the weight using a Gaussian function with a standard deviation of 1.

  Args:
      distance: (float) The distance to be used in the Gaussian function.
      theta: (float) The scale parameter for the Gaussian function.

  Returns:
      weight: (float) The weight calculated using the Gaussian function.
  """

  return np.exp(-(distance**2) / (2 * theta**2))


def functional_sensing(node_positions: np.ndarray, path_table: dict, probe_positions: np.ndarray,
                       probe_data: dict, probe_amplitudes: np.ndarray) -> np.ndarray:
  """
  Calculates the Electrogram (EGM) data for each probe, considering local signal influence
  and pacing artifact contribution based on probe positions, path information, and pacing signal amplitudes.

  Args:
      node_positions: (np.ndarray) A 2D array where each row represents the (x, y) coordinates of a node.
      path_table: (dict) A dictionary containing information about paths between nodes.
                  - Key: Path identifier.
                  - Value: A dictionary with path details (e.g., connected nodes, timers).
      probe_positions: (np.ndarray) A 2D array where each row represents the (x, y) coordinates of a probe.
      probe_data: (dict) A dictionary containing information about each probe.
                  - Key: Probe identifier.
                  - Value: A dictionary with probe details (e.g., connected paths).
      probe_amplitudes: (np.ndarray) A 1D array containing the amplitude of the pacing signal for each probe.

  Returns:
      egm_data: (np.ndarray) A 1D array containing the calculated EGM data for each probe.
  """

  local_theta = 15  # Threshold distance for local signal (in some units)
  far_theta = 80    # Threshold distance for pacing artifact (in some units)

  egm_data = np.zeros(len(probe_data))

  for probe_id, probe_info in probe_data.items():
    connected_paths = probe_info.get("connected_paths", [])

    # Local signal contribution
    for path_id in connected_paths:
      path_details = path_table.get(path_id)
      if path_details is None:
        continue  # Skip if path information is missing

      wavefront_pos = calculate_wavefront_position(path_details, node_positions)

      for wf_pos in wavefront_pos:
        distance = np.linalg.norm(probe_positions[probe_id] - wf_pos)
        weight = gauss_weight(float(distance), local_theta)
        egm_data[probe_id] += weight * path_details.get("signal_strength", 0)

    # Pacing artifact contribution
    pacing_probe_indices = np.where(probe_amplitudes != 0)[0]
    for pacing_probe_id in pacing_probe_indices:
      distance = np.linalg.norm(probe_positions[probe_id] - probe_positions[pacing_probe_id])
      weight = 0.7 * gauss_weight(float(distance), far_theta)
      egm_data[probe_id] += weight * probe_amplitudes[pacing_probe_id]

  return egm_data


def calculate_wavefront_position(path_details: dict, node_positions: np.ndarray) -> list: # type: ignore
  """
  Calculates the wavefront position(s) on a path based on path type (e.g., Ante, Retro, Double) and timer information.

  Args:
      path_details: (dict) A dictionary containing information about a specific path.
          - start_node_id: (int) Identifier of the starting node for the path.
          - end_node_id: (int) Identifier of the ending node for the path.
          - path_type: (str) Type of the path (e.g., "Ante", "Retro", "Double").
          - current_timer: (float) Current timer value for the path (relevant for wavefront calculation).
          - default_timer: (float) Default timer value for the path (relevant for wavefront calculation).
  Returns:
      wavefront_pos: (list) A list containing the (x, y) coordinates of the wavefront(s) on the path,
                          or an empty list if required information is missing.
  """

  required_fields = {"start_node_id", "end_node_id", "path_type", "current_timer", "default_timer"}
  if not all(field in path_details for field in required_fields):
    return []  # Handle missing information

