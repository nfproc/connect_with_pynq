// knight rider (extended) circuit for PYNQ 2021.04.19 Naoki F., AIT
// ライセンスについては LICENSE.txt を参照してください．

module knight2_pynq (
    input  wire        CLK,
    input  wire        RESETN,
    input  wire [ 3:0] AXI_CTRL_AWADDR,
    input  wire [ 2:0] AXI_CTRL_AWPROT,
    input  wire        AXI_CTRL_AWVALID,
    output wire        AXI_CTRL_AWREADY,
    input  wire [31:0] AXI_CTRL_WDATA,
    input  wire [ 3:0] AXI_CTRL_WSTRB,
    input  wire        AXI_CTRL_WVALID,
    output wire        AXI_CTRL_WREADY,
    output wire [ 1:0] AXI_CTRL_BRESP,
    output wire        AXI_CTRL_BVALID,
    input  wire        AXI_CTRL_BREADY,
    input  wire [ 3:0] AXI_CTRL_ARADDR,
    input  wire [ 2:0] AXI_CTRL_ARPROT,
    input  wire        AXI_CTRL_ARVALID,
    output wire        AXI_CTRL_ARREADY,
    output wire [31:0] AXI_CTRL_RDATA,
    output wire [ 1:0] AXI_CTRL_RRESP,
    output wire        AXI_CTRL_RVALID,
    input  wire        AXI_CTRL_RREADY,
    output reg   [3:0] LED);

    wire  [1:0] pattern;
    wire [31:0] cdiv;

    AXI_ctrl ctrl (
        .AXI_CTRL_ACLK   (CLK),
        .AXI_CTRL_ARESETN(RESETN),
        .AXI_CTRL_AWADDR (AXI_CTRL_AWADDR),
        .AXI_CTRL_AWPROT (AXI_CTRL_AWPROT),
        .AXI_CTRL_AWVALID(AXI_CTRL_AWVALID),
        .AXI_CTRL_AWREADY(AXI_CTRL_AWREADY),
        .AXI_CTRL_WDATA  (AXI_CTRL_WDATA),
        .AXI_CTRL_WSTRB  (AXI_CTRL_WSTRB),
        .AXI_CTRL_WVALID (AXI_CTRL_WVALID),
        .AXI_CTRL_WREADY (AXI_CTRL_WREADY),
        .AXI_CTRL_BRESP  (AXI_CTRL_BRESP),
        .AXI_CTRL_BVALID (AXI_CTRL_BVALID),
        .AXI_CTRL_BREADY (AXI_CTRL_BREADY),
        .AXI_CTRL_ARADDR (AXI_CTRL_ARADDR),
        .AXI_CTRL_ARPROT (AXI_CTRL_ARPROT),
        .AXI_CTRL_ARVALID(AXI_CTRL_ARVALID),
        .AXI_CTRL_ARREADY(AXI_CTRL_ARREADY),
        .AXI_CTRL_RDATA  (AXI_CTRL_RDATA),
        .AXI_CTRL_RRESP  (AXI_CTRL_RRESP),
        .AXI_CTRL_RVALID (AXI_CTRL_RVALID),
        .AXI_CTRL_RREADY (AXI_CTRL_RREADY),
        .KNIGHT_PATTERN  (pattern),
        .KNIGHT_CDIV     (cdiv));

    reg [31:0] count, n_count;
    reg  [2:0] pos, n_pos;
    
    always @ (pattern, pos) begin
        if (pattern == 2'd0) begin
            LED = 4'd0000;
        end else if (pattern == 2'd1) begin
            case (pos)
                3'd0: LED = 4'b0001;
                3'd1: LED = 4'b0010;
                3'd2: LED = 4'b0100;
                3'd3: LED = 4'b1000;
                3'd4: LED = 4'b0100;
                3'd5: LED = 4'b0010;
                default: LED = 4'b0000;
            endcase
        end else if (pattern == 2'd2) begin
            case (pos)
                3'd0: LED = 4'b1111;
                3'd1: LED = 4'b1110;
                3'd2: LED = 4'b1100;
                3'd3: LED = 4'b1000;
                3'd4: LED = 4'b1100;
                3'd5: LED = 4'b1110;
                default: LED = 4'b0000;
            endcase
        end else if (pattern == 2'd3) begin
            case (pos)
                3'd0: LED = 4'b0001;
                3'd1: LED = 4'b0011;
                3'd2: LED = 4'b0111;
                3'd3: LED = 4'b1111;
                3'd4: LED = 4'b0111;
                3'd5: LED = 4'b0011;
                default: LED = 4'b0000;
            endcase
        end
    end

    always @ (cdiv, count, pos) begin
        if (count >= cdiv) begin
            n_count = 1;
            if (pos == 3'd5) begin
                n_pos   = 3'd0;
            end else begin
                n_pos   = pos + 1'b1;
            end
        end else begin
            n_count = count + 1'b1;
            n_pos   = pos;
        end
    end

    always @ (posedge CLK) begin
        if (~ RESETN) begin
            count <= 0;
            pos   <= 3'd0;
        end else begin
            count <= n_count;
            pos   <= n_pos;
        end
    end
endmodule